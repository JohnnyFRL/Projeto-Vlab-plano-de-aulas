import { useNavigate } from "react-router-dom";
import styles from "./PlanCard.module.css";

function formatDate(str) {
  if (!str) return "—";
  const [y, m, d] = str.split("-");
  return `${d}/${m}/${y}`;
}

export default function PlanCard({ plan, onDelete }) {
  const navigate = useNavigate();
  const tags = plan.tags ? plan.tags.split(",").map((t) => t.trim()).filter(Boolean) : [];

  function handleDelete(e) {
    e.stopPropagation();
    if (window.confirm(`Remover "${plan.title}"?`)) {
      onDelete(plan.id);
    }
  }

  return (
    <div className={styles.card} onClick={() => navigate(`/planos/${plan.id}/editar`)}>
      <div className={styles.header}>
        <span className={styles.discipline}>{plan.discipline}</span>
        <span className={styles.date}>{formatDate(plan.planned_date)}</span>
      </div>

      <h3 className={styles.title}>{plan.title}</h3>

      <p className={styles.summary}>{plan.summary}</p>

      {tags.length > 0 && (
        <div className={styles.tags}>
          {tags.slice(0, 4).map((tag) => (
            <span key={tag} className={styles.tag}>{tag}</span>
          ))}
          {tags.length > 4 && (
            <span className={styles.tagMore}>+{tags.length - 4}</span>
          )}
        </div>
      )}

      <div className={styles.footer}>
        <button
          className={styles.editBtn}
          onClick={(e) => { e.stopPropagation(); navigate(`/planos/${plan.id}/editar`); }}
        >
          Editar
        </button>
        <button className={styles.deleteBtn} onClick={handleDelete}>
          Remover
        </button>
      </div>
    </div>
  );
}
