'use client';

import { useState, useRef, useEffect } from 'react';
import { useSession } from '@/lib/auth-client';
import { Send, User, Bot, Loader2, Plus, Trash2, MessageSquare } from 'lucide-react';
import { apiRequest, getConversations, getConversationMessages, deleteConversation, type Conversation, type ConversationMessage } from '@/lib/api';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export default function ChatPage() {
    const { data: session } = useSession();
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingConversations, setIsLoadingConversations] = useState(true);
    const [selectedModel, setSelectedModel] = useState('gemini-2.5-flash-lite');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const availableModels = [
        { id: 'gemini-2.5-flash-lite', name: 'Gemini 2.5 Flash Lite' },
        { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash' },
        { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro' },
        { id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash' },
    ];

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Load conversations on mount
    useEffect(() => {
        if (session?.user?.id) {
            loadConversations();
        }
    }, [session?.user?.id]);

    const loadConversations = async () => {
        if (!session?.user?.id) return;

        try {
            setIsLoadingConversations(true);
            const convs = await getConversations(session.user.id);
            setConversations(convs);
        } catch (error) {
            console.error('Failed to load conversations:', error);
        } finally {
            setIsLoadingConversations(false);
        }
    };

    const loadConversationMessages = async (conversationId: string) => {
        if (!session?.user?.id) return;

        try {
            setIsLoading(true);
            const msgs = await getConversationMessages(session.user.id, conversationId);
            setMessages(msgs.map(msg => ({
                id: msg.id,
                role: msg.role,
                content: msg.content,
                timestamp: new Date(msg.created_at)
            })));
            setActiveConversationId(conversationId);
        } catch (error) {
            console.error('Failed to load messages:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNewConversation = () => {
        setActiveConversationId(null);
        setMessages([]);
    };

    const handleDeleteConversation = async (conversationId: string, e: React.MouseEvent) => {
        e.stopPropagation();
        if (!session?.user?.id) return;

        if (!confirm('Are you sure you want to delete this conversation?')) return;

        try {
            await deleteConversation(session.user.id, conversationId);
            if (activeConversationId === conversationId) {
                handleNewConversation();
            }
            await loadConversations();
        } catch (error) {
            console.error('Failed to delete conversation:', error);
        }
    };

    const handleSendMessage = async (e?: React.FormEvent) => {
        e?.preventDefault();

        if (!input.trim() || !session?.user?.id) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await apiRequest<{ response: string; success: boolean; conversation_id: string }>(
                `/api/${session.user.id}/chat`,
                {
                    method: 'POST',
                    body: JSON.stringify({
                        message: userMessage.content,
                        conversation_id: activeConversationId,
                        model: selectedModel
                    }),
                }
            );

            if (response.success) {
                const botMessage: Message = {
                    id: (Date.now() + 1).toString(),
                    role: 'assistant',
                    content: response.response,
                    timestamp: new Date(),
                };
                setMessages(prev => [...prev, botMessage]);

                // Update active conversation ID if it's a new conversation
                if (!activeConversationId && response.conversation_id) {
                    setActiveConversationId(response.conversation_id);
                }

                // Reload conversations to update the list
                await loadConversations();
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: "Sorry, I encountered an error processing your request.",
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-[calc(100vh-8rem)] gap-6 p-2">
            {/* Conversations Sidebar */}
            <div className="w-85 glass-panel flex flex-col overflow-hidden transition-all duration-300 hover:shadow-glow">
                <div className="p-6 border-b border-primary-100/20 bg-white/10">
                    <div className="flex items-center justify-between mb-2">
                        <h2 className="text-xl font-bold text-gradient">Conversations</h2>
                        <button
                            onClick={handleNewConversation}
                            className="p-2 hover:bg-primary-100/30 rounded-xl transition-all duration-200 active:scale-95"
                            title="New Conversation"
                        >
                            <Plus className="w-6 h-6 text-primary-600" />
                        </button>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-3 space-y-2 custom-scrollbar">
                    {isLoadingConversations ? (
                        <div className="flex items-center justify-center h-32">
                            <Loader2 className="w-8 h-8 animate-spin text-primary-400" />
                        </div>
                    ) : conversations.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-48 text-primary-300/60 px-6">
                            <div className="p-4 bg-primary-50 rounded-full mb-4">
                                <MessageSquare className="w-10 h-10" />
                            </div>
                            <p className="text-sm font-medium text-center">No conversations yet</p>
                            <p className="text-xs text-center mt-1">Start a wave of ideas!</p>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {conversations.map((conv) => (
                                <div
                                    key={conv.id}
                                    onClick={() => loadConversationMessages(conv.id)}
                                    className={`p-4 rounded-xl cursor-pointer transition-all duration-200 group relative overflow-hidden ${activeConversationId === conv.id
                                        ? 'bg-gradient-to-r from-primary-500/10 to-secondary-500/10 border border-primary-200/50 shadow-sm'
                                        : 'hover:bg-white/40 border border-transparent'
                                        }`}
                                >
                                    {activeConversationId === conv.id && (
                                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-500 rounded-full" />
                                    )}
                                    <div className="flex items-start justify-between gap-3">
                                        <div className="flex-1 min-w-0">
                                            <h3 className={`font-semibold truncate text-sm ${activeConversationId === conv.id ? 'text-primary-700' : 'text-gray-700'}`}>
                                                {conv.title}
                                            </h3>
                                            <div className="flex items-center gap-2 mt-1">
                                                <span className="text-[10px] px-2 py-0.5 bg-primary-50 text-primary-600 rounded-full font-medium">
                                                    {conv.message_count} msgs
                                                </span>
                                                <span className="text-[10px] text-gray-400">
                                                    {new Date(conv.updated_at).toLocaleDateString()}
                                                </span>
                                            </div>
                                        </div>
                                        <button
                                            onClick={(e) => handleDeleteConversation(conv.id, e)}
                                            className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-50 rounded-lg transition-all duration-200"
                                            title="Delete conversation"
                                        >
                                            <Trash2 className="w-4 h-4 text-red-400 hover:text-red-600" />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col gap-4">
                <div className="flex items-center justify-between px-2">
                    <div>
                        <h1 className="text-3xl font-extrabold text-gradient tracking-tight">AI Navigator</h1>
                        <p className="text-sm text-primary-600/70 font-medium">Charting your tasks with intelligence.</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <select
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                            className="bg-white/50 backdrop-blur-sm border border-primary-100 rounded-full px-4 py-2 text-xs font-semibold text-primary-700 outline-none focus:ring-2 focus:ring-primary-500/20 transition-all cursor-pointer hover:bg-white/80"
                        >
                            {availableModels.map(model => (
                                <option key={model.id} value={model.id}>{model.name}</option>
                            ))}
                        </select>
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/50 backdrop-blur-sm rounded-full border border-primary-100 shadow-sm">
                            <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse" />
                            <span className="text-xs font-semibold text-primary-700">System Online</span>
                        </div>
                    </div>
                </div>

                <div className="flex-1 glass-panel flex flex-col overflow-hidden relative">
                    {/* Background Decorative Elements */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-primary-200/10 rounded-full blur-3xl -z-10" />
                    <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary-200/10 rounded-full blur-3xl -z-10" />

                    {/* Chat Messages Area */}
                    <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                        {messages.length === 0 ? (
                            <div className="h-full flex flex-col items-center justify-center text-primary-300/80">
                                <div className="w-20 h-20 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-3xl flex items-center justify-center mb-6 shadow-lg rotate-3">
                                    <Bot className="w-10 h-10 text-primary-600" />
                                </div>
                                <h3 className="text-xl font-bold text-primary-800 mb-2">Ready to Dive In?</h3>
                                <p className="text-center max-w-xs text-sm font-medium">I can help you manage your tasks with simple commands.</p>
                                <div className="mt-8 grid grid-cols-1 gap-3 w-full max-w-sm">
                                    <div className="p-3 bg-white/40 border border-primary-100 rounded-xl text-xs font-medium text-primary-700 hover:bg-white/60 transition-colors cursor-pointer">
                                        "Add a task to prepare for the deep sea dive"
                                    </div>
                                    <div className="p-3 bg-white/40 border border-primary-100 rounded-xl text-xs font-medium text-primary-700 hover:bg-white/60 transition-colors cursor-pointer">
                                        "List all my pending tasks"
                                    </div>
                                </div>
                            </div>
                        ) : (
                            messages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`flex items-start gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''
                                        } animate-in fade-in slide-in-from-bottom-2 duration-300`}
                                >
                                    <div
                                        className={`w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-sm ${msg.role === 'user'
                                            ? 'bg-gradient-to-br from-primary-500 to-primary-700 text-white'
                                            : 'bg-gradient-to-br from-secondary-400 to-secondary-600 text-white'
                                            }`}
                                    >
                                        {msg.role === 'user' ? (
                                            <User className="w-6 h-6" />
                                        ) : (
                                            <Bot className="w-6 h-6" />
                                        )}
                                    </div>
                                    <div
                                        className={`max-w-[75%] p-4 rounded-2xl shadow-sm relative ${msg.role === 'user'
                                            ? 'bg-gradient-to-br from-primary-600 to-primary-800 text-white rounded-tr-none'
                                            : 'bg-white/80 backdrop-blur-md text-gray-800 border border-primary-100 rounded-tl-none'
                                            }`}
                                    >
                                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                                        <div className={`text-[10px] mt-2 font-medium ${msg.role === 'user' ? 'text-primary-100' : 'text-gray-400'}`}>
                                            {msg.timestamp.toLocaleTimeString([], {
                                                hour: '2-digit',
                                                minute: '2-digit',
                                            })}
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                        {isLoading && (
                            <div className="flex items-start gap-4 animate-pulse">
                                <div className="w-10 h-10 rounded-2xl bg-secondary-100 flex items-center justify-center flex-shrink-0">
                                    <Bot className="w-6 h-6 text-secondary-400" />
                                </div>
                                <div className="bg-white/60 backdrop-blur-sm p-4 rounded-2xl rounded-tl-none border border-primary-50">
                                    <div className="flex gap-1">
                                        <div className="w-2 h-2 bg-secondary-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <div className="w-2 h-2 bg-secondary-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <div className="w-2 h-2 bg-secondary-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-6 bg-white/30 backdrop-blur-xl border-t border-primary-100/30">
                        <form onSubmit={handleSendMessage} className="flex gap-3 max-w-4xl mx-auto">
                            <div className="relative flex-1 group">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Type your command..."
                                    className="input-luxury pr-12 text-sm font-medium"
                                    disabled={isLoading}
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-primary-300 group-focus-within:text-primary-500 transition-colors">
                                    <MessageSquare className="w-5 h-5" />
                                </div>
                            </div>
                            <button
                                type="submit"
                                disabled={isLoading || !input.trim()}
                                className="btn-luxury !px-6 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                            >
                                {isLoading ? (
                                    <Loader2 className="w-6 h-6 animate-spin" />
                                ) : (
                                    <Send className="w-6 h-6" />
                                )}
                            </button>
                        </form>
                        <p className="text-[10px] text-center mt-3 text-primary-400 font-medium">
                            Powered by AI Navigator • Charting your productivity
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
