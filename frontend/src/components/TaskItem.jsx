import { updateTask, deleteTask } from "../api";
import { useState } from "react";

const TaskItem = ({ task, refreshTasks, token }) => {
    const [isUpdating, setIsUpdating] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    const toggleStatus = async () => {
      await updateTask(task.id, { completed: !task.completed }, token);  // ✅ Send only completed
      refreshTasks();
  };

    const removeTask = async () => {
        if (window.confirm("Are you sure you want to delete this task?")) {
            setIsDeleting(true);
            try {
                await deleteTask(task.id, token);
                refreshTasks();
            } catch (error) {
                console.error("Failed to delete task:", error);
            }
            setIsDeleting(false);
        }
    };

    return (
        <li className="p-4 border rounded shadow-md flex justify-between items-center">
            <div>
                <strong>{task.title}</strong> - {task.priority} - 
                {task.completed ? "✅ Completed" : "⏳ Pending"}
            </div>
            <div>
                <button 
                    onClick={toggleStatus} 
                    disabled={isUpdating} 
                    className={`px-3 py-1 text-white rounded ${isUpdating ? "bg-gray-400" : "bg-green-500 hover:bg-green-600"}`}
                >
                    {isUpdating ? "Updating..." : task.completed ? "Mark as Pending" : "Mark as Completed"}
                </button>
                <button 
                    onClick={removeTask} 
                    disabled={isDeleting} 
                    className={`ml-2 px-3 py-1 text-white rounded ${isDeleting ? "bg-gray-400" : "bg-red-500 hover:bg-red-600"}`}
                >
                    {isDeleting ? "Deleting..." : "🗑️ Delete"}
                </button>
            </div>
        </li>
    );
};

export default TaskItem;
