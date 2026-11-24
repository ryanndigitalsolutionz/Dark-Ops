
export default function Table({
  columns = [],
  data = [],
  loading = false,
  emptyMessage = "No records found.",
  rowKey = "id",
  onRowClick,
  selectedRows = [],
  onSelectionChange,
  className = "",
}) {
  const selectable = Boolean(onSelectionChange);

  const getRowId = (row, index) => row[rowKey] ?? index;

  const isSelected = (id) => selectedRows.includes(id);

  const toggleRow = (id) => {
    if (isSelected(id)) {
      onSelectionChange(selectedRows.filter((item) => item !== id));
    } else {
      onSelectionChange([...selectedRows, id]);
    }
  };

  const allSelected =
    data.length > 0 &&
    data.every((row, index) => isSelected(getRowId(row, index)));

  const toggleAll = () => {
    if (allSelected) {
      onSelectionChange([]);
    } else {
      onSelectionChange(data.map(getRowId));
    }
  };

  return (
    <div className={`w-full overflow-x-auto rounded-xl border border-zinc-800 ${className}`}>
      <table className="w-full border-collapse text-left text-sm">
        <thead className="bg-[#1c1f26]">
          <tr>
            {selectable && (
              <th className="w-12 px-4 py-3">
                <input
                  type="checkbox"
                  checked={allSelected}
                  onChange={toggleAll}
                  aria-label="Select all rows"
                  className="accent-[var(--color-agency-orange)]"
                />
              </th>
            )}

            {columns.map((column) => (
              <th
                key={column.key}
                className={`whitespace-nowrap px-4 py-3 font-semibold text-gray-300 ${column.headerClassName || ""}`}
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>

        <tbody className="divide-y divide-zinc-800 bg-[var(--color-agency-card)]">
          {loading ? (
            <tr>
              <td
                colSpan={columns.length + (selectable ? 1 : 0)}
                className="px-4 py-10 text-center text-gray-500"
              >
                <span className="inline-flex items-center justify-center gap-2">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[var(--color-agency-orange)]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[var(--color-agency-orange)] [animation-delay:150ms]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[var(--color-agency-orange)] [animation-delay:300ms]" />
                </span>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length + (selectable ? 1 : 0)}
                className="px-4 py-10 text-center text-gray-500"
              >
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row, index) => {
              const id = getRowId(row, index);

              return (
                <tr
                  key={id}
                  onClick={() => onRowClick?.(row)}
                  className={`text-gray-300 ${onRowClick ? "cursor-pointer" : ""} ${isSelected(id) ? "bg-orange-950/20" : ""}`}
                >
                  {selectable && (
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={isSelected(id)}
                        onChange={() => toggleRow(id)}
                        onClick={(event) => event.stopPropagation()}
                        aria-label={`Select row ${index + 1}`}
                        className="accent-[var(--color-agency-orange)]"
                      />
                    </td>
                  )}

                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={`px-4 py-3 ${column.className || ""}`}
                    >
                      {column.render
                        ? column.render(row, index)
                        : row[column.key] ?? "—"}
                    </td>
                  ))}
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
