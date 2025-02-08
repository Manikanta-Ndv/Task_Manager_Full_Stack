import { useState, useContext } from "react";
import { loginUser } from "../api";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(formData);
      login(res.data.access_token);
      navigate("/dashboard");
    } catch (error) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md bg-white/20 backdrop-blur-lg p-8 shadow-lg rounded-2xl border border-white/30"
      >
        <h2 className="text-3xl font-bold text-center text-white mb-6">
          Welcome Back👋
        </h2>

        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              className="w-full px-4 py-3 bg-white/20 border border-white/40 rounded-lg text-white placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <input
              type="password"
              name="password"
              placeholder="Password"
              className="w-full px-4 py-3 bg-white/20 border border-white/40 rounded-lg text-white placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
              onChange={handleChange}
              required
            />
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            className="w-full bg-white/30 text-white py-3 rounded-lg font-semibold hover:bg-white/40 transition-all shadow-md"
          >
            Login
          </motion.button>
        </form>

        <p className="text-center text-sm text-white mt-4">
          Don't have an account?{" "}
          <a href="/register" className="text-white font-semibold hover:underline">
            Register here
          </a>
        </p>
      </motion.div>
    </div>
  );
};

export default Login;
