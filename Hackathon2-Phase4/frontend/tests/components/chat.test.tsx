import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import ChatPage from '@/app/chat/page';
import ChatWindow from '@/app/chat/components/ChatWindow';
import { MessageComponent } from '@/app/chat/components/Message';
import NewChatButton from '@/app/chat/components/NewChatButton';
import ConversationList from '@/app/chat/components/ConversationList';
import { useChat } from '@/app/chat/hooks/useChat';

// Mock the useChat hook
vi.mock('@/app/chat/hooks/useChat', () => ({
  useChat: vi.fn()
}));

// Mock the router
vi.mock('next/navigation', () => ({
  useRouter: vi.fn(() => ({
    push: vi.fn(),
  })),
  usePathname: vi.fn(() => '/chat'),
}));

describe('Chat Components', () => {
  const mockUseChat = {
    messages: [
      { id: '1', role: 'user', content: 'Hello', timestamp: '2023-01-01T00:00:00Z' },
      { id: '2', role: 'assistant', content: 'Hi there!', timestamp: '2023-01-01T00:00:01Z' },
    ],
    sendMessage: vi.fn(),
    currentConversationId: 'conv-123',
    createNewConversation: vi.fn(),
    isLoading: false,
    loadConversationHistory: vi.fn(),
  };

  beforeEach(() => {
    (useChat as vi.Mock).mockReturnValue(mockUseChat);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('ChatPage', () => {
    it('renders the chat page with header and chat window', () => {
      render(<ChatPage />);

      expect(screen.getByText('AI Todo Assistant')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /new chat/i })).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    });

    it('calls createNewConversation when new chat button is clicked', () => {
      render(<ChatPage />);

      const newChatButton = screen.getByRole('button', { name: /new chat/i });
      fireEvent.click(newChatButton);

      expect(mockUseChat.createNewConversation).toHaveBeenCalledTimes(1);
    });
  });

  describe('ChatWindow', () => {
    it('displays messages correctly', () => {
      render(
        <ChatWindow
          messages={mockUseChat.messages}
          onSendMessage={mockUseChat.sendMessage}
          currentConversationId={mockUseChat.currentConversationId}
          isLoading={mockUseChat.isLoading}
        />
      );

      expect(screen.getByText('Hello')).toBeInTheDocument();
      expect(screen.getByText('Hi there!')).toBeInTheDocument();
    });

    it('handles sending a message', async () => {
      render(
        <ChatWindow
          messages={mockUseChat.messages}
          onSendMessage={mockUseChat.sendMessage}
          currentConversationId={mockUseChat.currentConversationId}
          isLoading={mockUseChat.isLoading}
        />
      );

      const input = screen.getByPlaceholderText('Type your message here...');
      const sendButton = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, { target: { value: 'Test message' } });
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(mockUseChat.sendMessage).toHaveBeenCalledWith('Test message');
      });
    });

    it('shows loading state when isLoading is true', () => {
      render(
        <ChatWindow
          messages={mockUseChat.messages}
          onSendMessage={mockUseChat.sendMessage}
          currentConversationId={mockUseChat.currentConversationId}
          isLoading={true}
        />
      );

      expect(screen.getByText('Thinking...')).toBeInTheDocument();
    });
  });

  describe('MessageComponent', () => {
    it('renders user message with correct styling', () => {
      const userMessage = { id: '1', role: 'user', content: 'Hello', timestamp: '2023-01-01T00:00:00Z' };

      render(<MessageComponent message={userMessage} />);

      const messageElement = screen.getByText('Hello');
      expect(messageElement).toHaveClass('bg-blue-500'); // User messages should have blue background
    });

    it('renders assistant message with correct styling', () => {
      const assistantMessage = { id: '2', role: 'assistant', content: 'Hi there!', timestamp: '2023-01-01T00:00:01Z' };

      render(<MessageComponent message={assistantMessage} />);

      const messageElement = screen.getByText('Hi there!');
      expect(messageElement).toHaveClass('bg-gray-200'); // Assistant messages should have gray background
    });
  });

  describe('NewChatButton', () => {
    it('renders the new chat button', () => {
      const mockOnCreateNew = vi.fn();

      render(<NewChatButton onCreateNew={mockOnCreateNew} />);

      const button = screen.getByRole('button', { name: /new chat/i });
      expect(button).toBeInTheDocument();
    });

    it('calls onCreateNew when clicked', () => {
      const mockOnCreateNew = vi.fn();

      render(<NewChatButton onCreateNew={mockOnCreateNew} />);

      const button = screen.getByRole('button', { name: /new chat/i });
      fireEvent.click(button);

      expect(mockOnCreateNew).toHaveBeenCalledTimes(1);
    });
  });

  describe('ConversationList', () => {
    it('renders conversations list when conversations exist', () => {
      const mockConversations = [
        { id: 'conv-1', title: 'First conversation', created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' },
        { id: 'conv-2', title: 'Second conversation', created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' },
      ];

      // Mock fetch call
      global.fetch = vi.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve(mockConversations),
          ok: true,
        } as Response)
      ) as vi.Mock;

      render(
        <ConversationList
          onSelectConversation={vi.fn()}
          currentConversationId="conv-1"
        />
      );

      expect(screen.getByText('First conversation')).toBeInTheDocument();
      expect(screen.getByText('Second conversation')).toBeInTheDocument();
    });

    it('shows loading state initially', () => {
      render(
        <ConversationList
          onSelectConversation={vi.fn()}
          currentConversationId="conv-1"
        />
      );

      expect(screen.getByText('Loading conversations...')).toBeInTheDocument();
    });
  });
});

describe('useChat Hook', () => {
  it('should initialize with empty messages', () => {
    const { result } = renderHook(() => useChat());

    expect(result.current.messages).toEqual([]);
  });

  it('should send a message', async () => {
    const { result } = renderHook(() => useChat());

    act(() => {
      result.current.sendMessage('Test message');
    });

    await waitFor(() => {
      expect(result.current.messages).toHaveLength(2); // User message + simulated response
    });
  });

  it('should create a new conversation', () => {
    const { result } = renderHook(() => useChat());

    act(() => {
      result.current.createNewConversation();
    });

    expect(result.current.messages).toEqual([]);
    expect(result.current.currentConversationId).toBeUndefined();
  });
});