import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query";
import { Sparkles, Eye, Code, Palette, Tag as TagIcon, Save, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const cardSchema = z.object({
  deck_id: z.string().min(1, "Please select a deck"),
  front_title: z.string().min(1, "Title is required").max(100),
  back_content: z.string().min(1, "Prompt content is required"),
  tags: z.string().optional(),
  front_background_url: z.string().url().optional().or(z.literal("")),
});

interface CardBuilderProps {
  defaultDeckId?: string;
  children?: React.ReactNode;
}

export function CardBuilder({ defaultDeckId, children }: CardBuilderProps) {
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();

  // Fetch decks for the selector
  const { data: decks } = useQuery({
    queryKey: ["decks"],
    queryFn: async () => {
      const response = await api.get("/decks");
      return response.data;
    },
    enabled: open,
  });

  const form = useForm<z.infer<typeof cardSchema>>({
    resolver: zodResolver(cardSchema),
    defaultValues: {
      deck_id: defaultDeckId || "",
      front_title: "",
      back_content: "",
      tags: "",
      front_background_url: "",
    },
  });

  const mutation = useMutation({
    mutationFn: (values: z.infer<typeof cardSchema>) => {
      return api.post("/cards", values);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cards"] });
      setOpen(false);
      form.reset();
    },
  });

  function onSubmit(values: z.infer<typeof cardSchema>) {
    mutation.mutate(values);
  }

  const watchContent = form.watch("back_content");
  const watchTitle = form.watch("front_title");

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button variant="default">
            <Sparkles className="mr-2 h-4 w-4" /> Create Card
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="max-w-6xl h-[90vh] flex flex-col p-0 overflow-hidden">
        <DialogHeader className="p-6 border-b flex flex-row items-center justify-between">
          <div>
            <DialogTitle className="text-2xl font-bold flex items-center gap-2">
              <Sparkles className="h-6 w-6 text-primary" />
              Card Builder
            </DialogTitle>
          </div>
          <Button variant="ghost" size="icon" onClick={() => setOpen(false)} className="rounded-full">
            <X className="h-5 w-5" />
          </Button>
        </DialogHeader>

        <div className="flex-1 flex overflow-hidden">
          {/* Form Side */}
          <div className="w-1/2 overflow-y-auto border-r p-6">
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <Tabs defaultValue="content" className="w-full">
                  <TabsList className="grid w-full grid-cols-3 mb-4">
                    <TabsTrigger value="content" className="flex items-center gap-2">
                      <Code className="h-4 w-4" /> Content
                    </TabsTrigger>
                    <TabsTrigger value="design" className="flex items-center gap-2">
                      <Palette className="h-4 w-4" /> Design
                    </TabsTrigger>
                    <TabsTrigger value="meta" className="flex items-center gap-2">
                      <TagIcon className="h-4 w-4" /> Meta
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="content" className="space-y-4 pt-2">
                    <FormField
                      control={form.control}
                      name="deck_id"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Target Deck</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder="Select a deck to add this card to" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {decks?.map((deck: any) => (
                                <SelectItem key={deck.id} value={deck.id}>
                                  {deck.name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="front_title"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Card Title</FormLabel>
                          <FormControl>
                            <Input placeholder="E.g., Cyberpunk Street Scene" {...field} />
                          </FormControl>
                          <FormDescription>The name displayed on the front of the card.</FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="back_content"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Prompt Content (Markdown)</FormLabel>
                          <FormControl>
                            <Textarea 
                              placeholder="Paste your prompt here... Markdown is supported!" 
                              className="min-h-[300px] font-mono text-sm leading-relaxed"
                              {...field} 
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </TabsContent>

                  <TabsContent value="design" className="space-y-4 pt-2">
                    <FormField
                      control={form.control}
                      name="front_background_url"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Artwork URL</FormLabel>
                          <FormControl>
                            <Input placeholder="https://images.unsplash.com/..." {...field} />
                          </FormControl>
                          <FormDescription>Optional background image for the card front.</FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <div className="p-4 rounded-lg bg-muted/50 text-sm text-muted-foreground">
                      Advanced customization (colors, borders, frames) coming soon in Phase 3B.
                    </div>
                  </TabsContent>

                  <TabsContent value="meta" className="space-y-4 pt-2">
                    <FormField
                      control={form.control}
                      name="tags"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Tags (Comma separated)</FormLabel>
                          <FormControl>
                            <Input placeholder="cyberpunk, futuristic, neon" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </TabsContent>
                </Tabs>

                <div className="pt-4 border-t flex items-center justify-between">
                  <p className="text-xs text-muted-foreground flex items-center gap-1">
                    <Sparkles className="h-3 w-3" /> Auto-embedding enabled
                  </p>
                  <Button type="submit" size="lg" disabled={mutation.isPending}>
                    {mutation.isPending ? "Saving..." : (
                      <>
                        <Save className="mr-2 h-4 w-4" /> Save Card
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </Form>
          </div>

          {/* Preview Side */}
          <div className="w-1/2 bg-muted/30 p-8 flex items-center justify-center overflow-y-auto">
            <div className="w-full max-w-[350px] space-y-4">
              <div className="flex items-center gap-2 mb-4 text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                <Eye className="h-4 w-4" /> Live Preview
              </div>
              
              <Tabs defaultValue="front">
                <TabsList className="w-full mb-4">
                  <TabsTrigger value="front" className="flex-1">Front (Visual)</TabsTrigger>
                  <TabsTrigger value="back" className="flex-1">Back (Prompt)</TabsTrigger>
                </TabsList>
                
                <TabsContent value="front">
                  <div className="aspect-[2.5/3.5] rounded-2xl border-8 border-primary bg-card shadow-2xl overflow-hidden relative group">
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent z-10" />
                    <div className="absolute inset-0 bg-muted">
                      {form.watch("front_background_url") ? (
                        <img 
                          src={form.watch("front_background_url")} 
                          alt="Preview" 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center opacity-20">
                           <Sparkles className="h-20 w-20" />
                        </div>
                      )}
                    </div>
                    <div className="absolute bottom-0 left-0 right-0 p-6 z-20">
                      <div className="text-xs font-bold text-primary-foreground/70 uppercase mb-1 tracking-widest">PROMPT CARD</div>
                      <div className="text-2xl font-black text-white leading-tight break-words">
                        {watchTitle || "Untitled Prompt"}
                      </div>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="back">
                  <div className="aspect-[2.5/3.5] rounded-2xl border-4 border-muted bg-card shadow-2xl p-6 overflow-hidden flex flex-col">
                    <div className="text-xs font-bold text-muted-foreground uppercase mb-4 border-b pb-2">Prompt Details</div>
                    <div className="flex-1 overflow-y-auto prose prose-sm dark:prose-invert">
                      {watchContent ? (
                        <ReactMarkdown className="text-sm leading-relaxed text-card-foreground">
                          {watchContent}
                        </ReactMarkdown>
                      ) : (
                        <p className="text-muted-foreground italic">No content yet...</p>
                      )}
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
              
              <p className="text-center text-xs text-muted-foreground italic">
                Cards will use the 384-dimensional local embedding model for semantic search accuracy.
              </p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
