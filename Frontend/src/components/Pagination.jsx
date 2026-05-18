import styles from "./Pagination.module.css";

export default function Pagination({ page, pages, total, onChange }) {
  if (pages <= 1) return null;

  return (
    <div className={styles.row}>
      <span className={styles.info}>{total} planos</span>

      <div className={styles.controls}>
        <button
          className={styles.btn}
          disabled={page <= 1}
          onClick={() => onChange(page - 1)}
        >
          ← Anterior
        </button>

        <span className={styles.current}>
          {page} / {pages}
        </span>

        <button
          className={styles.btn}
          disabled={page >= pages}
          onClick={() => onChange(page + 1)}
        >
          Próxima →
        </button>
      </div>
    </div>
  );
}
