import * as styles from "./styles.css.ts";

document.body.className = styles.body;

document.body.innerHTML = `
  <div class="${styles.card}">
    <div class="${styles.cardBody}">
      <span class="${styles.badge}">New</span>
      <h2 class="${styles.cardTitle}">Wireless Headphones</h2>
      <p class="${styles.cardDescription}">
        Premium sound quality with active noise cancellation and 30-hour battery life.
      </p>

      <div class="${styles.cardMeta}">
        <span class="${styles.price}">$129.00</span>
        <span class="${styles.rating}">★ 4.8</span>
      </div>

      <div class="${styles.tags}">
        <span class="${styles.tag}">Audio</span>
        <span class="${styles.tag}">Wireless</span>
      </div>

      <button class="${styles.btnPrimary}">Add to Cart</button>
    </div>
  </div>
`;
