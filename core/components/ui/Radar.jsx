
export default function Spinner({
  size = "md",
  className = "",
  color = "var(--color-agency-orange)",
}) {
  const sizes = {
    xs: "h-3 w-3 border",
    sm: "h-4 w-4 border-2",
    md: "h-6 w-6 border-2",
    lg: "h-9 w-9 border-[3px]",
    xl: "h-12 w-12 border-4",
  };

  return (
    <span
      role="status"
      aria-label="Loading"
      className={`inline-block shrink-0 animate-spin rounded-full border-current border-t-transparent ${sizes[size] || sizes.md} ${className}`}
      style={{ color }}
    />
  );
}
