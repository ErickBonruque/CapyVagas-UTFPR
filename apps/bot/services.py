import logging
from apps.users.models import UserProfile
from apps.users.services import UTFPRAuthService
from apps.courses.models import Course, SearchTerm
from infra.jobspy.service import JobSearchService
from infra.waha.client import WahaClient
from apps.bot.models import BotConfiguration, InteractionLog

logger = logging.getLogger(__name__)

class BotService:
    """
    Controla o fluxo de conversação do bot.
    """

    BRAND_HEADER = (
        "🌟 CapyVagas | Assistente de Vagas da UTFPR\n"
        "Conecto você às oportunidades certas para o seu curso."
    )
    
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
        if text in {"menu", "ajuda", "help", "opcoes", "opções"}:
            self.send_menu(user, chat_id)
            return

        if text in {"2", "sair", "logout"}:
            self.handle_logout(user, chat_id)
            return

        if self.handle_pending_action(user, chat_id, text):
            return

        if text in {"1", "cadastrar", "login"}:
            self.start_login_flow(user, chat_id)
            return

        if text in {"3", "curso", "cursos"}:
            self.start_course_selection(user, chat_id)
            return

        if not user.is_authenticated_utfpr:
            self.start_login_flow(user, chat_id)
            return

        self.send_menu(user, chat_id)

    def start_login_flow(self, user: UserProfile, chat_id: str) -> None:
        """Exibe instruções e marca o estado de coleta de credenciais."""

        user.current_action = "awaiting_credentials"
        user.save(update_fields=["current_action", "last_activity"])
        prompt = (
            f"{self.BRAND_HEADER}\n\n"
            "Opção 1) Cadastro do aluno.\n"
            "Envie o RA e a senha do Portal do Aluno separados por espaço (ex: a1234567 minhaSenha)."
        )
        self.waha_client.send_message(chat_id, prompt)
        self._log_sent(user, prompt)

    def attempt_login(self, user: UserProfile, chat_id: str, text: str) -> None:
        """Realiza autenticação com RA e senha."""

        parts = text.split()
        if len(parts) != 2:
            reminder = (
                "Formato inválido. Envie RA e senha separados por espaço (ex: a1234567 minhaSenha)."
            )
            self.waha_client.send_message(chat_id, reminder)
            self._log_sent(user, reminder)
            return

        ra, password = parts
        if self.auth_service.authenticate(ra, password):
            self.auth_service.link_user(chat_id, ra, password)
            user.refresh_from_db()
            user.current_action = None
            user.save(update_fields=["current_action", "last_activity"])
            success_message = (
                "✅ Cadastro confirmado! Use a opção 3 para escolher seu curso e termo de busca, "
                "ou envie 'menu' para rever as opções."
            )
            self.waha_client.send_message(chat_id, success_message)
            self._log_sent(user, success_message)
        else:
            failure = "❌ Falha no login. Verifique RA e senha e tente novamente (Formato: RA SENHA)."
            self.waha_client.send_message(chat_id, failure)
            self._log_sent(user, failure)

    def handle_logout(self, user, chat_id):
        self.auth_service.logout(chat_id)
        self.waha_client.send_message(chat_id, "🔒 Você saiu do sistema. Até logo!")
        self._log_sent(user, "🔒 Você saiu do sistema. Até logo!")
        user.current_action = None
        user.selected_course = None
        user.selected_term = None
        user.save(update_fields=["current_action", "selected_course", "selected_term", "last_activity"])

    def start_course_selection(self, user: UserProfile, chat_id: str) -> None:
        """Apresenta cursos disponíveis para usuários autenticados."""

        if not user.is_authenticated_utfpr:
            need_login = (
                "🔐 Você precisa se cadastrar primeiro (opção 1) para escolher curso e termo."
            )
            self.waha_client.send_message(chat_id, need_login)
            self._log_sent(user, need_login)
            return

        courses = list(Course.objects.filter(is_active=True).order_by("order", "name"))
        if not courses:
            no_courses = "⚠️ Nenhum curso configurado ainda. Cadastre pelo dashboard."
            self.waha_client.send_message(chat_id, no_courses)
            self._log_sent(user, no_courses)
            return

        menu_lines = [f"{idx+1}) {course.name}" for idx, course in enumerate(courses)]
        message = (
            f"{self.BRAND_HEADER}\n\nOpção 3) Escolha seu curso:\n" + "\n".join(menu_lines)
            + "\n\nEnvie o número do curso desejado."
        )

        user.current_action = "awaiting_course_choice"
        user.save(update_fields=["current_action", "last_activity"])
        self.waha_client.send_message(chat_id, message)
        self._log_sent(user, message)

    def handle_course_choice(self, user: UserProfile, chat_id: str, text: str) -> None:
        courses = list(Course.objects.filter(is_active=True).order_by("order", "name"))
        if not courses:
            self.start_course_selection(user, chat_id)
            return

        try:
            index = int(text) - 1
        except ValueError:
            reminder = "Envie apenas o número do curso que deseja selecionar."
            self.waha_client.send_message(chat_id, reminder)
            self._log_sent(user, reminder)
            return

        if index < 0 or index >= len(courses):
            invalid = "Opção inválida. Escolha um número da lista enviada."
            self.waha_client.send_message(chat_id, invalid)
            self._log_sent(user, invalid)
            return

        course = courses[index]
        user.selected_course = course
        user.current_action = "awaiting_term_choice"
        user.save(update_fields=["selected_course", "current_action", "last_activity"])

        terms = list(course.search_terms.order_by("-priority", "term"))
        if not terms:
            no_terms = (
                "⚠️ Este curso ainda não tem termos de busca configurados. Ajuste pelo dashboard."
            )
            self.waha_client.send_message(chat_id, no_terms)
            self._log_sent(user, no_terms)
            user.current_action = None
            user.save(update_fields=["current_action"])
            return

        term_lines = [f"{idx+1}) {term.term}" for idx, term in enumerate(terms)]
        message = (
            f"Curso selecionado: {course.name}.\nAgora escolha o termo para buscar vagas:\n"
            + "\n".join(term_lines)
            + "\n\nEnvie o número do termo desejado."
        )
        self.waha_client.send_message(chat_id, message)
        self._log_sent(user, message)

    def handle_term_choice(self, user: UserProfile, chat_id: str, text: str) -> None:
        if not user.selected_course:
            self.start_course_selection(user, chat_id)
            return

        terms = list(
            SearchTerm.objects.filter(course=user.selected_course).order_by("-priority", "term")
        )
        if not terms:
            self.start_course_selection(user, chat_id)
            return

        try:
            index = int(text) - 1
        except ValueError:
            reminder = "Envie apenas o número do termo que deseja usar."
            self.waha_client.send_message(chat_id, reminder)
            self._log_sent(user, reminder)
            return

        if index < 0 or index >= len(terms):
            invalid = "Opção inválida. Escolha um número da lista enviada."
            self.waha_client.send_message(chat_id, invalid)
            self._log_sent(user, invalid)
            return

        term = terms[index]
        user.selected_term = term
        user.current_action = None
        user.save(update_fields=["selected_term", "current_action", "last_activity"])

        jobs = self.job_service.search([term.term], limit=5)
        if not jobs:
            no_jobs = (
                f"😔 Nada encontrado para {term.term} no momento. Tente outro termo ou volte mais tarde."
            )
            self.waha_client.send_message(chat_id, no_jobs)
            self._log_sent(user, no_jobs)
            return

        response_lines = [
            f"🎓 Vagas para {user.selected_course.name} | Termo: {term.term}",
            "-----------------------------------",
        ]
        for job in jobs:
            response_lines.append(
                f"🏢 {job['company']}\n💼 {job['title']}\n🔗 {job['url']}"
            )

        response_lines.append("Envie 'menu' para novas opções ou '3' para outra busca.")
        response = "\n\n".join(response_lines)
        self.waha_client.send_message(chat_id, response)
        self._log_sent(user, response)

    def send_menu(self, user: UserProfile, chat_id: str) -> None:
        """Exibe menu com identidade CapyVagas e opções principais."""

        menu = (
            f"{self.BRAND_HEADER}\n\n"
            "Escolha uma opção:\n"
            "1) Cadastrar o aluno (RA + senha do Portal do Aluno)\n"
            "2) Logout\n"
            "3) Selecionar curso e termo para buscar vagas\n\n"
            "Envie 'menu' a qualquer momento para ver as opções."
        )

        if not user.is_authenticated_utfpr:
            menu += "\n\n🔐 Você ainda não está autenticado. Use a opção 1 para conectar."

        self.waha_client.send_message(chat_id, menu)
        self._log_sent(user, menu)

    def _log_sent(self, user: UserProfile, message: str) -> None:
        InteractionLog.objects.create(
            user=user,
            message_content=message,
            message_type="SENT",
            session_id=self.waha_client.settings.session_name,
        )

    def handle_pending_action(self, user: UserProfile, chat_id: str, text: str) -> bool:
        """Executa ações que dependem de um estado anterior."""

        if user.current_action == "awaiting_credentials":
            self.attempt_login(user, chat_id, text)
            return True

        if user.current_action == "awaiting_course_choice":
            self.handle_course_choice(user, chat_id, text)
            return True

        if user.current_action == "awaiting_term_choice":
            self.handle_term_choice(user, chat_id, text)
            return True

        return False
