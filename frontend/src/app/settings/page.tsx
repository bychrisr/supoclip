"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useSession } from "@/lib/auth-client";
import { toast } from "sonner";
import { Loader2, Save, Youtube, ShieldCheck, ExternalLink, ArrowLeft, Key, Sparkles, Brain, Zap } from "lucide-react";
import Link from "next/link";

export default function SettingsPage() {
  const { data: session, isPending: isLoadingSession } = useSession();
  const [youtubeCookies, setYoutubeCookies] = useState("");
  const [assemblyKey, setAssemblyKey] = useState("");
  const [googleKey, setGoogleKey] = useState("");
  const [openrouterKey, setOpenrouterKey] = useState("");
  
  const [isSaving, setIsSaving] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [status, setStatus] = useState<Record<string, boolean>>({});

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (session?.user && isLoading) {
      console.log("🔍 [Settings] Buscando configurações (Cache-Bust)...");
      // Add timestamp to prevent browser cache
      fetch(`/api/settings/info?t=${Date.now()}`, {
        headers: { "user_id": session.user.id },
        cache: "no-store" // Next.js 15+ Cache Override
      })
      .then(res => res.json())
      .then(data => {
        console.log("📦 [Settings] Dados recebidos:", data);
        setStatus({
          youtube: data.youtube_cookies_active,
          assembly: data.assembly_ai_active,
          google: data.google_active,
          openrouter: data.openrouter_active
        });
        
        console.log("📊 [Settings] Status das chaves:", data);

        if (data.youtube_cookies && !data.youtube_cookies.startsWith("sk-")) {
          setYoutubeCookies(data.youtube_cookies);
        }
        
        // Always set placeholders if active to show feedback to user
        if (data.assembly_ai_active) setAssemblyKey("********************************");
        if (data.google_active) setGoogleKey("********************************");
        if (data.openrouter_active) setOpenrouterKey("********************************");
      })
      .catch(err => console.error("❌ [Settings] Erro ao buscar configurações", err))
      .finally(() => setIsLoading(false));
    }
  }, [session, isLoading]);

  const handleSaveField = async (provider: string, value: string) => {
    if (!session?.user) return;
    setIsSaving(provider);
    console.log(`🚀 [Settings] Salvando chave para: ${provider}...`);
    
    try {
      const response = await fetch(`/api/settings/${provider}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "text/plain",
          "user_id": session.user.id
        },
        body: value
      });

      if (response.ok) {
        toast.success(`${provider.toUpperCase()} atualizado com sucesso!`);
        setStatus(prev => ({ ...prev, [provider]: true }));
        console.log(`✅ [Settings] ${provider} persistido no banco.`);
      } else {
        toast.error(`Falha ao salvar ${provider}.`);
      }
    } catch (error) {
      console.error(`❌ [Settings] Erro ao salvar ${provider}:`, error);
      toast.error("Erro de conexão.");
    } finally {
      setIsSaving(null);
    }
  };

  if (isLoading || isLoadingSession) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-stone-50">
        <Loader2 className="w-8 h-8 animate-spin text-orange-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-stone-50 text-stone-900 pb-20">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="mb-8">
          <Link href="/" className="flex items-center text-sm text-stone-500 hover:text-orange-600 transition-colors mb-4">
            <ArrowLeft className="w-4 h-4 mr-1" />
            Voltar para o Estúdio
          </Link>
          <h1 className="text-4xl font-bold font-syne tracking-tight">Configurações</h1>
          <p className="text-stone-500 mt-2 text-lg">Gerencie suas chaves de API e integrações (BYOK).</p>
        </div>

        <div className="grid gap-6">
          {/* YouTube Section */}
          <Card className="border-stone-200 shadow-sm overflow-hidden">
            <CardHeader className="bg-white border-b border-stone-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-red-50 rounded-full flex items-center justify-center">
                  <Youtube className="text-red-600 w-6 h-6" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <CardTitle className="text-xl font-syne">YouTube Bypass</CardTitle>
                    {status.youtube && <Badge className="bg-green-500 text-[10px] uppercase">Ativo</Badge>}
                  </div>
                  <CardDescription>Cookies para evitar bloqueios de download.</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              <Textarea 
                placeholder="# Netscape HTTP Cookie File..." 
                className="min-h-[150px] font-mono text-xs bg-stone-50"
                value={youtubeCookies}
                onChange={(e) => setYoutubeCookies(e.target.value)}
              />
              <Button 
                onClick={() => handleSaveField("youtube", youtubeCookies)} 
                disabled={isSaving === "youtube"}
                className="w-full bg-stone-900 hover:bg-stone-800"
              >
                {isSaving === "youtube" ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Save className="w-4 h-4 mr-2" />}
                Salvar Cookies
              </Button>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Google Gemini */}
            <Card className="border-stone-200 shadow-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-blue-500" />
                    <CardTitle className="text-lg font-syne">Google Gemini</CardTitle>
                  </div>
                  {status.google && <Badge className="bg-green-500 text-[10px]">Ativo</Badge>}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <Input 
                  type="password" 
                  placeholder="AI Studio API Key"
                  value={googleKey}
                  onChange={(e) => setGoogleKey(e.target.value)}
                />
                <Button 
                  onClick={() => handleSaveField("google", googleKey)}
                  disabled={isSaving === "google"}
                  variant="outline" 
                  className="w-full border-stone-300"
                >
                  {isSaving === "google" ? <Loader2 className="w-4 h-4 animate-spin" /> : "Salvar Chave"}
                </Button>
              </CardContent>
            </Card>

            {/* AssemblyAI */}
            <Card className="border-stone-200 shadow-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-orange-500" />
                    <CardTitle className="text-lg font-syne">AssemblyAI</CardTitle>
                  </div>
                  {status.assembly && <Badge className="bg-green-500 text-[10px]">Ativo</Badge>}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <Input 
                  type="password" 
                  placeholder="AssemblyAI API Key"
                  value={assemblyKey}
                  onChange={(e) => setAssemblyKey(e.target.value)}
                />
                <Button 
                  onClick={() => handleSaveField("assembly", assemblyKey)}
                  disabled={isSaving === "assembly"}
                  variant="outline" 
                  className="w-full border-stone-300"
                >
                  {isSaving === "assembly" ? <Loader2 className="w-4 h-4 animate-spin" /> : "Salvar Chave"}
                </Button>
              </CardContent>
            </Card>

            {/* OpenRouter */}
            <Card className="border-stone-200 shadow-sm md:col-span-2">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-500" />
                    <CardTitle className="text-lg font-syne">OpenRouter (Fallback)</CardTitle>
                  </div>
                  {status.openrouter && <Badge className="bg-green-500 text-[10px]">Ativo</Badge>}
                </div>
                <CardDescription>Usado automaticamente caso o Gemini atinja o limite de cota.</CardDescription>
              </CardHeader>
              <CardContent className="flex gap-4">
                <Input 
                  type="password" 
                  placeholder="OpenRouter API Key"
                  className="flex-1"
                  value={openrouterKey}
                  onChange={(e) => setOpenrouterKey(e.target.value)}
                />
                <Button 
                  onClick={() => handleSaveField("openrouter", openrouterKey)}
                  disabled={isSaving === "openrouter"}
                  className="bg-purple-600 hover:bg-purple-700 text-white"
                >
                  {isSaving === "openrouter" ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4 mr-2" />}
                  Salvar
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
