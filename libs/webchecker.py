import idna
import requests
import whois


class Webchecker:
    """
    Main class, used to represent testing of availability domain
    """

    def __init__(self):
        self.HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }

    @staticmethod
    def correct_puny(domain):
        """
        Convert punny code into available domain
        :param domain: plain text which consist domain
        :return: correct domain
        """
        if domain.startswith('xn--'):
            domain = idna.decode(domain)
        return domain

    def check_status(self, domain):
        """
        Checking status code of domain
        :param domain: domain
        :return: status code, if check failed - return 999
        """
        try:
            domain = self.correct_puny(domain)
            if not domain.startswith('http'):
                domain = 'http://' + domain
            req = requests.get(domain, self.HEADERS)
            return req.status_code
        except:
            return 999

    def get_expiration_date(self, domain):
        """
        Checking expiration date
        :param domain: domain
        :return: string with expiration date
        """
        try:
            domain = self.correct_puny(domain)
            who = whois.whois(domain)
            if isinstance(who.expiration_date, list):
                ex_date_tmp = who.expiration_date[0]
            else:
                ex_date_tmp = who.expiration_date
            return ex_date_tmp
        except:
            return -1

    def check_tag(self, domain, tag):
        """
        Check consisting of tag in main page of domain
        :param domain: domain
        :param tag: tag which we looking for
        :return: index of tag or -1 in case if not found
        """
        try:
            domain = self.correct_puny(domain)
            if not domain.startswith('http'):
                domain = 'http://' + domain
            req = requests.get(domain, self.HEADERS)
            return req.text.find(tag)
        except:
            return -1
