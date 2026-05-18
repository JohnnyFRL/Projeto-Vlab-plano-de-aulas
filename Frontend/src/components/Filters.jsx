import styles from "./Filters.module.css";

export default function Filters({ filters, onChange }) {
  function handle(e) {
    onChange({ ...filters, [e.target.name]: e.target.value, page: 1 });
  }

  return (
    <div className={styles.row}>
      <input
        className={styles.search}
        name="search"
        value={filters.search}
        onChange={handle}
        placeholder="Buscar por título..."
      />

      <input
        className={styles.field}
        name="discipline"
        value={filters.discipline}
        onChange={handle}
        placeholder="Disciplina"
      />

      <input
        className={styles.field}
        name="tag"
        value={filters.tag}
        onChange={handle}
        placeholder="Tag"
      />

      <input
        className={styles.field}
        type="date"
        name="planned_date"
        value={filters.planned_date}
        onChange={handle}
      />

      <select className={styles.field} name="sort" value={filters.sort} onChange={handle}>
        <option value="created_at">Mais recentes</option>
        <option value="title">Título (A–Z)</option>
        <option value="planned_date">Data prevista</option>
      </select>
    </div>
  );
}
