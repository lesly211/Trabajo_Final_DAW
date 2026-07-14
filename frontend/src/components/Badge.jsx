import { estadoBadge } from "../utils/format";
export default function Badge({ estado }) {
  return <span className={`badge ${estadoBadge(estado)}`}>{estado}</span>;
}
