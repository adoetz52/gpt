import React, { useState } from 'react';
import { MessageCircle, Send, Bot, User, CheckCircle2, LoaderCircle, SidebarClose, SidebarOpen } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

// Mock data for demonstration
const initialModels = [
  { id: 'gemini', name: 'Gemini Flash', color: 'bg-blue-500', type: 'manual' },
  { id: 'gpt4', name: 'GPT-4 Mini', color: 'bg-green-500', type: 'manual' },
  { id: 'grok', name: 'Grok AI', color: 'bg-purple-500', type: 'manual' },
  { id: 'phi', name: 'Phi 3.5', color: 'bg-orange-500', type: 'manual' },
  { id: 'llama', name: 'Llama 405B', color: 'bg-red-500', type: 'manual' },
  { id: 'auto1', name: 'Auto Model 1', color: 'bg-teal-500', type: 'auto' },
  { id: 'auto2', name: 'Auto Model 2', color: 'bg-indigo-500', type: 'auto' },
];

const initialMessages = [
  { id: 1, text: 'Hello! How can I help you today?', sender: 'bot', model: 'Gemini Flash' },
  { id: 2, text: 'Can you explain quantum computing?', sender: 'user' },
  { id: 3, text: 'Quantum computing is a type of computing that uses quantum phenomena such as superposition and entanglement...', sender: 'bot', model: 'Gemini Flash' },
];

const TelegramDashboard = () => {
  const [selectedModel, setSelectedModel] = useState(initialModels[0]);
  const [messages, setMessages] = useState(initialMessages);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  
  const handleSend = async () => {
    if (!inputText.trim()) return;
    
    const newUserMessage = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user'
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setInputText('');
    setIsLoading(true);
    
    // Simulate bot response
    setTimeout(() => {
      const newBotMessage = {
        id: messages.length + 2,
        text: `Response from ${selectedModel.name}: This is a simulated response.`,
        sender: 'bot',
        model: selectedModel.name
      };
      setMessages(prev => [...prev, newBotMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-white border-r border-gray-200 overflow-hidden`}>
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Bot className="w-6 h-6 text-blue-500" />
            <h2 className="text-lg font-semibold">Model Selection</h2>
          </div>
        </div>
        <div className="p-2">
          {initialModels.map(model => (
            <button
              key={model.id}
              onClick={() => setSelectedModel(model)}
              className={`w-full p-3 mb-2 rounded-lg flex items-center space-x-3 transition-colors
                ${selectedModel.id === model.id ? 'bg-blue-50' : 'hover:bg-gray-50'}`}
            >
              <div className={`w-3 h-3 rounded-full ${model.color}`} />
              <span className="flex-1 text-left text-sm">{model.name}</span>
              {selectedModel.id === model.id && (
                <CheckCircle2 className="w-4 h-4 text-blue-500" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <button 
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              {isSidebarOpen ? <SidebarClose className="w-5 h-5" /> : <SidebarOpen className="w-5 h-5" />}
            </button>
            <div className="flex items-center space-x-2">
              <MessageCircle className="w-5 h-5 text-blue-500" />
              <h1 className="text-lg font-semibold">Telegram Bot Dashboard</h1>
            </div>
          </div>
          <Alert className="w-auto">
            <AlertDescription className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${selectedModel.color}`} />
              <span>Using {selectedModel.name}</span>
            </AlertDescription>
          </Alert>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(message => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] p-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-gray-200'
                }`}
              >
                {message.sender === 'bot' && (
                  <div className="flex items-center space-x-2 mb-1">
                    <Bot className="w-4 h-4 text-blue-500" />
                    <span className="text-xs text-gray-500">{message.model}</span>
                  </div>
                )}
                <p className="text-sm">{message.text}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 p-3 rounded-lg flex items-center space-x-2">
                <LoaderCircle className="w-4 h-4 animate-spin text-blue-500" />
                <span className="text-sm text-gray-500">Generating response...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your message..."
                className="w-full p-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                rows="1"
              />
            </div>
            <button
              onClick={handleSend}
              disabled={isLoading || !inputText.trim()}
              className={`px-4 py-2 rounded-lg flex items-center space-x-2 ${
                isLoading || !inputText.trim()
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
            >
              {isLoading ? (
                <LoaderCircle className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TelegramDashboard;
