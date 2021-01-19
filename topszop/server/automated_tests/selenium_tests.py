from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class AuthenticationTests(StaticLiveServerTestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName='runTest')
        #dane konta testowego
        self.username = "test"
        self.email = "test@test.com"
        self.test_pass = "test_pass"

    @classmethod
    def setUpClass(cls):
        #otwieramy przeglÄ…darkÄ™
        super(AuthenticationTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        #zamykamy przeglÄ…darkÄ™
        cls.selenium.quit()
        super(AuthenticationTests, cls).tearDownClass()

    def runTest(self):
        #tworzenie uÅ¼ytkownika
        user = User.objects.create_superuser(self.username, self.email, self.test_pass)
        user.save()

        #prÃ³ba zalogowania
        self.selenium.get("%s/admin" % self.live_server_url)
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.test_pass)
        self.selenium.find_element_by_css_selector("input[type='submit']").click()

        #czekamy aÅ¼ zaÅ‚aduje siÄ™ strona panelu
        WebDriverWait(self.selenium, 2).until(lambda driver: driver.find_element_by_css_selector("#content h1"))

        #sprawdzamy czy jesteÅ›my na stronie panelu
        self.assertEqual("Site administration", self.selenium.find_element_by_css_selector("#content h1").text)

        #sprzÄ…tamy
        user.delete()
