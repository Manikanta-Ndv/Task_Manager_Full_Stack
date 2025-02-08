import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

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
            await axios.post(
                "http://localhost:8000/tasks/",
                { title, description, priority, due_date: dueDate, assigned_to: assignedTo },
                { headers: { Authorization: `Bearer ${token}` } }
            );

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
        <motion.form
            onSubmit={handleSubmit}
            className="bg-white/30 backdrop-blur-md p-6 shadow-lg rounded-2xl border border-white/30 max-w-lg mx-auto"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <h2 className="text-2xl font-semibold text-gray-800 text-center mb-5"> Create a New Task</h2>

            {/* Title */}
            <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">Task Title</label>
                <input
                    type="text"
                    placeholder="Enter task title..."
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    className="w-full p-3 rounded-lg border bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            {/* Description */}
            <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">Description</label>
                <textarea
                    placeholder="Enter task description..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                    rows={3}
                    className="w-full p-3 rounded-lg border bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            {/* Priority Dropdown */}
            <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">Priority</label>
                <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    required
                    className="w-full p-3 rounded-lg border bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                    <option value="High"> High</option>
                    <option value="Medium"> Medium</option>
                    <option value="Low"> Low</option>
                </select>
            </div>

            {/* Due Date */}
            <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">Due Date</label>
                <input
                    type="date"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                    required
                    className="w-full p-3 rounded-lg border bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            {/* Assigned To */}
            <div className="mb-6">
                <label className="block text-gray-700 font-medium mb-2">Assign To</label>
                <input
                    type="text"
                    placeholder="Enter email or name..."
                    value={assignedTo}
                    onChange={(e) => setAssignedTo(e.target.value)}
                    required
                    className="w-full p-3 rounded-lg border bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            {/* Submit Button */}
            <motion.button
                type="submit"
                disabled={isSubmitting}
                className="w-full p-3 text-white font-semibold rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 hover:opacity-90 transition-all"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                {isSubmitting ? "Creating..." : "Create Task"}
            </motion.button>
        </motion.form>
    );
};

export default TaskForm;
