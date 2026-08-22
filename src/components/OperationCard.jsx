import React, { useState } from "react";

function OperationCard({ mission, onUpdateMission, onDeleteMission }) {
  if (!mission) return null;
  
  const { id, title, description } = mission;
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title || "");
  const [editDesc, setEditDesc] = useState(description || "");

  function handleSave() {
    onUpdateMission({ id, title: editTitle, description: editDesc });
    setIsEditing(false);
  }

  function handleWipe() {
    onDeleteMission(id);
  }

  if (isEditing) {
    return (
      <div className="mission-card">
        <div>
          <input
            type="text"
            className="ops-input"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
          />
          <textarea
            className="ops-input"
            rows="3"
            value={editDesc}
            onChange={(e) => setEditDesc(e.target.value)}
          />
        </div>
        <div className="card-actions">
          <button className="ops-btn btn-sm btn-orange" onClick={handleSave}>Commit</button>
          <button className="ops-btn btn-sm" onClick={() => setIsEditing(false)}>Cancel</button>
        </div>
      </div>
    );
  }

  return (
    <div className="mission-card">
      <div>
        <div className="card-header">
          <div className="mission-indicator">Ø</div>
          <div className="mission-details">
            <h3>{title}</h3>
          </div>
        </div>
        <div className="mission-details">
          <p>{description}</p>
        </div>
      </div>
      
      <div className="card-actions">
        <button className="ops-btn btn-sm btn-orange" onClick={() => setIsEditing(true)}>Modify</button>
        <button className="ops-btn btn-sm" onClick={handleWipe}>Clear</button>
      </div>
    </div>
  );
}

export default OperationCard;
