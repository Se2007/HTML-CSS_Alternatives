import * as styles from './styles.css';

export default function ProductCard() {
  return (
    <div className={styles.body}>
      <div className={styles.card}>
        <div className={styles.cardBody}>
          <span className={styles.badge}>New</span>
          <h2 className={styles.cardTitle}>Wireless Headphones</h2>
          <p className={styles.cardDescription}>
            Premium sound quality with active noise cancellation and 30-hour battery life.
          </p>

          <div className={styles.cardMeta}>
            <span className={styles.price}>$129.00</span>
            <span className={styles.rating}>★ 4.8</span>
          </div>

          <div className={styles.tags}>
            <span className={styles.tag}>Audio</span>
            <span className={styles.tag}>Wireless</span>
          </div>

          <button className={styles.btnPrimary}>Add to Cart</button>
        </div>
      </div>
    </div>
  );
}
