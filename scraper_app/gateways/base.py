from abc import ABC

import cloudscraper
from requests.exceptions import InvalidSchema
from rich.console import Console

console = Console()


class BaseGateway(ABC):

    def make_request(self, url: str) -> str:
        '''
        Makes the request to the full_url using cloudscraper
        and returns the html in it.
        '''
        html = ''
        scraper = cloudscraper.create_scraper()
        console.log(
            'On my way to [bold cyan]GET[/bold cyan] [u]{}[/u]'.format(
                self._name
            )
        )

        try:
            res = scraper.get(url)
        except InvalidSchema as e:
            console.log(
                '[bold u]ERROR[/bold u]: {} raised InvalidSchema.\n {}'.format(
                     self._name, e
                )
            )

        if res.ok:
            html = res.text
            console.log(
                '{} responded OK!'.format(self._name),
                style='green'
            )
        else:
            console.log(
                (
                    '[bold u]ERROR[/bold u]: {} responded'
                    ' with error [red bold]{}[/red bold]!'.format(
                        self._name, res.status_code
                    )
                ),
                style='red'
            )

        return html