import { useQuery } from "@tanstack/react-query";
import { Plus, MoreVertical, LayoutGrid, List as ListIcon } from "lucide-react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Skeleton } from "@/components/ui/skeleton";

interface Deck {
  id: string;
  name: string;
  description: string;
  artwork_url?: string;
  created_at: string;
}

export default function HomePage() {
  const { data: decks, isLoading } = useQuery<Deck[]>({
    queryKey: ["decks"],
    queryFn: async () => {
      const response = await api.get("/decks");
      return response.data;
    },
  });

  return (
    <div className="flex-1 space-y-8 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Gallery</h2>
          <p className="text-muted-foreground">
            Manage your prompt decks and collect new prompts.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="icon">
            <LayoutGrid className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <ListIcon className="h-4 w-4" />
          </Button>
          <Button className="bg-primary hover:bg-primary/90">
            <Plus className="mr-2 h-4 w-4" /> New Deck
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="overflow-hidden shadow-md">
              <Skeleton className="h-48 w-full" />
              <CardHeader>
                <Skeleton className="h-6 w-1/2" />
                <Skeleton className="h-4 w-3/4" />
              </CardHeader>
            </Card>
          ))}
        </div>
      ) : decks?.length === 0 ? (
        <div className="flex min-h-[400px] flex-col items-center justify-center rounded-xl border border-dashed p-8 text-center animate-in fade-in zoom-in duration-300">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-muted">
            <LayoutGrid className="h-10 w-10 text-muted-foreground" />
          </div>
          <h3 className="mt-4 text-xl font-semibold">No decks found</h3>
          <p className="mb-6 mt-2 text-sm text-muted-foreground max-w-sm">
            You haven't created any prompt decks yet. Start by creating your first deck to organize your AI prompts.
          </p>
          <Button>
            <Plus className="mr-2 h-4 w-4" /> Create First Deck
          </Button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {decks?.map((deck) => (
            <Card key={deck.id} className="group overflow-hidden transition-all hover:shadow-xl hover:-translate-y-1 border-muted bg-card">
              <div className="relative h-48 w-full overflow-hidden bg-muted">
                {deck.artwork_url ? (
                  <img
                    src={deck.artwork_url}
                    alt={deck.name}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-primary/20 to-secondary/20">
                    <LayoutGrid className="h-12 w-12 text-primary/40" />
                  </div>
                )}
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <Button variant="secondary" className="font-semibold shadow-lg">View Deck</Button>
                </div>
              </div>
              <CardHeader className="flex flex-row items-start justify-between space-y-0 p-4">
                <div className="space-y-1">
                  <CardTitle className="text-xl group-hover:text-primary transition-colors">{deck.name}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    {deck.description || "No description provided."}
                  </CardDescription>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Edit Details</DropdownMenuItem>
                    <DropdownMenuItem>Duplicate Deck</DropdownMenuItem>
                    <DropdownMenuItem>Export to GitHub</DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </CardHeader>
              <CardFooter className="p-4 pt-0 text-xs text-muted-foreground flex justify-between items-center border-t border-muted/50 mt-2">
                <span>Created {new Date(deck.created_at).toLocaleDateString()}</span>
                <span className="bg-muted px-2 py-1 rounded-full font-medium">0 Cards</span>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
