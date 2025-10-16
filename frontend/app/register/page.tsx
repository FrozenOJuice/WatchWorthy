"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import "./register.css";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "member"
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Registration failed");
        setLoading(false);
        return;
      }

      alert("Registration successful! Please log in.");
      router.push("/login");
    } catch (err) {
      setError("Network error. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Create an Account</h2>

      <form onSubmit={handleSubmit} className="register-form">
        {error && <p className="error">{error}</p>}

        <label>
          Username:
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Email:
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Password:
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Role:
          <select name="role" value={form.role} onChange={handleChange}>
            <option value="member">Member</option>
            <option value="critic">Critic</option>
            <option value="moderator">Moderator</option>
            <option value="administrator">Administrator</option>
          </select>
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>

      <p className="redirect">
        Already have an account? <span onClick={() => router.push("/login")}>Log In</span>
      </p>
    </div>
  );
}
