
export default function Loading({ size = "md", className = "" }) {
  const sizes = {
    sm: "h-1.5 w-1.5",
    md: "h-2.5 w-2.5",
    lg: "h-3.5 w-3.5",
  };

  const dotSize = sizes[size] || sizes.md;

  return (
    <div
      role="status"
      aria-label="Loading"
      className={`flex items-center justify-center gap-2 ${className}`}
    >
      {[0, 1, 2].map((dot) => (
        <span
          key={dot}
          className={`${dotSize} animate-bounce rounded-full bg-[var(--color-agency-orange)]`}
          style={{ animationDelay: `${dot * 150}ms` }}
        />
      ))}
    </div>
  );
}
