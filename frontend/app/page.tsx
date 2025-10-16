"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import "./page.css";

export default function HomePage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      setIsAuthenticated(true);
      router.push("/dashboard");
    } else {
      setIsAuthenticated(false);
    }
  }, [router]);

  if (isAuthenticated === null) {
    return (
      <div className="loading-container">
        <h2>Loading...</h2>
      </div>
    );
  }

  return (
    <div className="homepage-container">
      <h2>Welcome to Movie Review Hub</h2>
      <p>
        Browse popular movies, read authentic reviews, and join our community of film enthusiasts. 
        Sign in to access your personalized dashboard, or continue as a guest.
      </p>

      <div className="button-group">
        <button onClick={() => router.push("/login")} className="btn btn-login">
          Log In
        </button>
        <button onClick={() => router.push("/register")} className="btn btn-register">
          Register
        </button>
        <button onClick={() => router.push("/movies")} className="btn btn-guest">
          Continue as Guest
        </button>
      </div>
    </div>
  );
}
