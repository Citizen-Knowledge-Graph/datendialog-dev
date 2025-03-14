
https://sozialplattform.de/content/de/api/v1/social-benefits-finder

```bash
python -m venv venv
source venv/bin/activate

python <script>.py
```

```js
// https://sozialplattform.de/inhalt/leistungsbereiche-der-uebersicht
// in the browser developer console:
let cards = document.getElementsByClassName('preview-card');
for (let i = 0; i < cards.length; i++) {
    let card = cards[i];
    let anchor = card.querySelector('a');
    let href = anchor.getAttribute('href');
    let title = card.querySelector('h3');
    console.log('URL:', href);
    console.log('Title:', title.textContent);
}
```
