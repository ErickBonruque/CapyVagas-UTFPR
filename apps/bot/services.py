import logging
from apps.users.models import UserProfile
from apps.users.services import UTFPRAuthService
from apps.courses.models import Course
from infra.jobspy.service import JobSearchService
from infra.waha.client import WahaClient
from apps.bot.models import BotConfiguration, InteractionLog

logger = logging.getLogger(__name__)

class BotService:
    """
    Controla o fluxo de conversação do bot.
    """
    
    def __init__(
        self,
        auth_service: UTFPRAuthService | None = None,
        job_service: JobSearchService | None = None,
        waha_client: WahaClient | None = None,
    ):
        waha_settings = BotConfiguration.get_active()
        self.auth_service = auth_service or UTFPRAuthService()
        self.job_service = job_service or JobSearchService()
        self.waha_client = waha_client or WahaClient(settings=waha_settings)

    def process_message(self, chat_id, message, from_me):
        """
        Processa uma mensagem recebida.
        """
        if from_me:
            return

        # Normalizar mensagem
        text = message.strip().lower()
        
        # Identificar usuário
        try:
            user = UserProfile.objects.get(phone_number=chat_id)
        except UserProfile.DoesNotExist:
            user = UserProfile.objects.create(phone_number=chat_id)

        InteractionLog.objects.create(
            user=user,
            message_content=message,
            message_type="RECEIVED",
            session_id=self.waha_client.settings.session_name,
        )

        # Fluxo de Comandos
        if text == 'sair' or text == 'logout':
            self.handle_logout(user, chat_id)
            return

        if not user.is_authenticated_utfpr:
            self.handle_login_flow(user, chat_id, text)
        else:
            self.handle_authenticated_flow(user, chat_id, text)

    def handle_login_flow(self, user, chat_id, text):
        """
        Gerencia o estado de login.
        """
        # Simplificação: Espera formato "RA SENHA"
        parts = text.split()
        if len(parts) == 2:
            ra, password = parts
            if self.auth_service.authenticate(ra, password):
                self.auth_service.link_user(chat_id, ra, password)
                success_message = "✅ Login realizado com sucesso! Digite 'vagas' para buscar oportunidades."
                self.waha_client.send_message(chat_id, success_message)
                self._log_sent(user, success_message)
            else:
                failure = "❌ Falha no login. Verifique RA e senha e tente novamente (Formato: RA SENHA)."
                self.waha_client.send_message(chat_id, failure)
                self._log_sent(user, failure)
        else:
            prompt = "👋 Olá! Para acessar, envie seu RA e Senha separados por espaço (Ex: a1234567 senha123)."
            self.waha_client.send_message(chat_id, prompt)
            self._log_sent(user, prompt)

    def handle_logout(self, user, chat_id):
        self.auth_service.logout(chat_id)
        self.waha_client.send_message(chat_id, "🔒 Você saiu do sistema. Até logo!")
        self._log_sent(user, "🔒 Você saiu do sistema. Até logo!")

    def handle_authenticated_flow(self, user, chat_id, text):
        """
        Menu principal para usuários logados.
        """
        if 'vaga' in text:
            self.waha_client.send_message(chat_id, "🔍 Buscando vagas para seus cursos de interesse...")
            
            # Exemplo: Buscar vagas para todos os cursos ativos
            # Em produção, perguntaria qual curso
            courses = Course.objects.filter(is_active=True)
            if not courses.exists():
                self.waha_client.send_message(chat_id, "⚠️ Nenhum curso configurado no sistema.")
                self._log_sent(user, "⚠️ Nenhum curso configurado no sistema.")
                return

            for course in courses:
                terms = list(course.search_terms.filter(is_default=True).values_list('term', flat=True))
                if terms:
                    jobs = self.job_service.search(terms, limit=3)
                    if jobs:
                        response = f"🎓 *Vagas para {course.name}:*\n\n"
                        for job in jobs:
                            response += f"🏢 *{job['company']}*\n💼 {job['title']}\n🔗 {job['url']}\n\n"
                        self.waha_client.send_message(chat_id, response)
                        self._log_sent(user, response)
                    else:
                        self.waha_client.send_message(chat_id, f"😔 Nenhuma vaga encontrada para {course.name} no momento.")
                        self._log_sent(user, f"😔 Nenhuma vaga encontrada para {course.name} no momento.")

        else:
            response = "🤖 Comandos disponíveis:\n- 'vagas': Buscar oportunidades\n- 'sair': Fazer logout"
            self.waha_client.send_message(chat_id, response)
            self._log_sent(user, response)

    def _log_sent(self, user: UserProfile, message: str) -> None:
        InteractionLog.objects.create(
            user=user,
            message_content=message,
            message_type="SENT",
            session_id=self.waha_client.settings.session_name,
        )
