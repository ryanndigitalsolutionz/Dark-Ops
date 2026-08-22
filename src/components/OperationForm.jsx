import { useState } from "react";

function OperationForm({ onAddMission }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim() || !description.trim()) return;

    onAddMission({ title, description });
    setTitle("");
    setDescription("");
  }

  return (
    <div className="ops-panel">
      <h2 className="panel-title">Initialize Operation</h2>
      <form onSubmit={handleSubmit}>
        <label className="text-sm tracking-wider uppercase text-gray-400">Operation Title</label>
        <input
          type="text"
          className="ops-input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        
        <label className="text-sm tracking-wider uppercase text-gray-400">Tactical Description</label>
        <textarea
          className="ops-input"
          rows="4"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        
        <button type="submit" className="ops-btn">Deploy</button>
      </form>
    </div>
  );
}

export default OperationForm;
