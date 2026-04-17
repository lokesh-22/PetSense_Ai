import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <main className="not-found">
      <p className="eyebrow">404</p>
      <h1>Page not found</h1>
      <p>The route does not exist yet in this frontend scaffold.</p>
      <Link to="/">Return to dashboard</Link>
    </main>
  );
}
