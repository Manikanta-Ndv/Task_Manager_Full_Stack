import React, { useState } from "react";
import axios from "axios";

const TaskForm = ({ refreshTasks }) => {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [priority, setPriority] = useState("Medium");
    const [dueDate, setDueDate] = useState("");
    const [assignedTo, setAssignedTo] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true); // Disable button while submitting

        const token = localStorage.getItem("token");

        try {
            const response = await axios.post(
                "http://localhost:8000/tasks/",
                {
                    title,
                    description,
                    priority,
                    due_date: dueDate,
                    assigned_to: assignedTo
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            console.log("Task created:", response.data);

            // Reset form fields
            setTitle("");
            setDescription("");
            setPriority("Medium");
            setDueDate("");
            setAssignedTo("");

            // Refresh task list
            refreshTasks();
        } catch (error) {
            console.error("Error creating task:", error.response?.data || error.message);
        }

        setIsSubmitting(false);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 shadow-lg rounded-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Create New Task</h2>

            {/* Title */}
            <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="w-full p-2 border rounded mb-3"
            />

            {/* Description */}
            <textarea
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
                className="w-full p-2 border rounded mb-3"
            />

            {/* Priority Dropdown */}
            <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                required
                className="w-full p-2 border rounded mb-3"
            >
                <option value="High"> High</option>
                <option value="Medium"> Medium</option>
                <option value="Low"> Low</option>
            </select>

            {/* Due Date */}
            <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                required
                className="w-full p-2 border rounded mb-3"
            />

            {/* Assigned To */}
            <input
                type="text"
                placeholder="Assign to (email or name)"
                value={assignedTo}
                onChange={(e) => setAssignedTo(e.target.value)}
                required
                className="w-full p-2 border rounded mb-3"
            />

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isSubmitting}
                className={`w-full p-2 text-white font-semibold rounded transition-all ${
                    isSubmitting ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                }`}
            >
                {isSubmitting ? "Creating..." : "Create Task"}
            </button>
        </form>
    );
};

export default TaskForm;
