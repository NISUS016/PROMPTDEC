import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Navbar } from "@/components/Navbar";
import HomePage from "@/pages/HomePage";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="relative flex min-h-screen flex-col">
          <Navbar />
          <SidebarProvider>
            <div className="flex flex-1">
              <AppSidebar />
              <main className="flex-1 overflow-auto bg-background/50">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/decks/:id" element={<div className="p-8 text-3xl font-bold">Deck View Placeholder</div>} />
                  <Route path="/cards/:id" element={<div className="p-8 text-3xl font-bold">Card View Placeholder</div>} />
                </Routes>
              </main>
            </div>
          </SidebarProvider>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;