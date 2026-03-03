from django.contrib.auth.mixins import UserPassesTestMixin


class CoordinadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticaated and (
            self.request.user.is_admin or self.request.user.es_coordinador()
        )

class VocalOSuperiorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticaated and (
            self.request.user.is_admin or
            self.request.user.es_coordinador() or
            self.request.user.es_vocal() or
            self.request.user.es_secretaria()
        )