import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

// Placeholder components (will move to separate files later)
const Home = () => (
  <div className="flex flex-col items-center justify-center min-h-screen p-4">
    <h1 className="text-4xl font-bold text-primary">PromptDec</h1>
    <p className="mt-2 text-muted-foreground">The TCG-style prompt gallery</p>
    <div className="mt-8 p-6 border rounded-xl shadow-lg bg-card">
      <p>Frontend Foundation Ready!</p>
    </div>
  </div>
);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/decks/:id" element={<div>Deck View Placeholder</div>} />
          <Route path="/cards/:id" element={<div>Card View Placeholder</div>} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;