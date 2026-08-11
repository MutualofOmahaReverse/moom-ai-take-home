import type { Loan } from "../lib/api";

export default function LoanList({
  loans,
  selected,
  onSelect,
}: {
  loans: Loan[];
  selected: number | null;
  onSelect: (id: number) => void;
}) {
  return (
    <div className="card">
      <h2>Loan files</h2>
      <table>
        <thead>
          <tr>
            <th>Reference</th>
            <th>Borrower</th>
            <th>Product</th>
            <th>Status</th>
            <th>Docs</th>
          </tr>
        </thead>
        <tbody>
          {loans.map((l) => (
            <tr
              key={l.id}
              className={selected === l.id ? "sel" : ""}
              onClick={() => onSelect(l.id)}
            >
              <td><code>{l.reference}</code></td>
              <td>{l.borrower_name}</td>
              <td>{l.product ?? <span className="pill none">unset</span>}</td>
              <td>{l.status ?? <span className="pill none">null</span>}</td>
              <td>{l.document_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
