import React, { useState } from 'react';

export default function App() {
  // State for mobile hamburger menu
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Darkened Palette Definitions (Used via Tailwind arbitrary values)
  // Base 1 (Plum) -> #4A3C45 : Main Background
  // Base 2 (Grey) -> #857F80 : Borders / Secondary UI
  // Base 3 (Rose) -> #98686A : User Bubbles
  // Base 4 (Coral) -> #D68F76 : Bot Bubbles
  // Base 5 (Cream) -> #E0CDA8 : Primary Text

  return (
    <div className="flex h-screen w-full bg-[#4A3C45] text-[#E0CDA8] font-sans overflow-hidden">
      
      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar Component */}
      <aside 
        className={`fixed inset-y-0 left-0 z-50 w-72 bg-[#4A3C45] border-r border-[#857F80] flex flex-col transition-transform duration-300 ease-in-out transform ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } md:relative md:translate-x-0`}
      >
        <div className="p-4 flex-grow flex flex-col gap-6">
          {/* New Conversation Button */}
          <button className="w-full py-3 px-4 border-2 border-[#857F80] rounded-xl text-left hover:bg-[#857F80] hover:text-[#4A3C45] transition-colors font-semibold">
            + New conversation
          </button>

          {/* Previous Conversations */}
          <div className="flex-grow">
            <h3 className="text-sm font-bold text-[#857F80] mb-3 uppercase tracking-wider">Previous</h3>
            <div className="space-y-3">
              <div className="h-10 border border-[#857F80] rounded-lg bg-opacity-20 bg-[#857F80]"></div>
              <div className="h-10 border border-[#857F80] rounded-lg bg-opacity-20 bg-[#857F80]"></div>
            </div>
          </div>

          {/* Model Selector */}
          <div className="mt-auto">
            <label className="block text-sm font-bold text-[#857F80] mb-2">Model</label>
            <select 
              className="w-full p-2 bg-[#4A3C45] border-2 border-[#857F80] rounded-lg text-[#E0CDA8] focus:outline-none focus:border-[#D68F76] appearance-none"
              defaultValue="someone900x"
            >
              <option value="someone900x">Someone900x</option>
            </select>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full relative">
        
        {/* Header Component */}
        <header className="flex items-center justify-between p-4 border-b border-[#857F80] bg-[#4A3C45]">
          <div className="flex items-center gap-4">
            {/* Hamburger Icon (Mobile Only) */}
            <button 
              className="md:hidden p-2 text-[#E0CDA8]"
              onClick={() => setIsSidebarOpen(true)}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <span className="font-mono text-sm border border-[#E0CDA8] px-2 py-1 rounded">BETA</span>
          </div>

          {/* Logo Placeholder - Designed for Asset Injection */}
          <div className="flex items-center gap-3">
            <div className="h-8 w-24 border border-dashed border-[#857F80] flex items-center justify-center text-xs font-bold text-[#857F80]">
              [LOGO.SVG]
            </div>
            <span className="text-sm text-[#857F80] hidden sm:block">Made for easy use</span>
          </div>
          
          <div className="w-10"> {/* Spacer to balance header flexbox */} </div>
        </header>

        {/* Chat Canvas */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 flex flex-col">
          
          {/* Bot Bubble (Ipsum) */}
          <div className="self-start max-w-[85%] md:max-w-[70%]">
            <div className="bg-[#D68F76] text-[#4A3C45] p-4 rounded-2xl rounded-tl-none shadow-md">
              <p>Ipsum. This is where the backend stream will render. We will hook this up to the someone900x model.</p>
            </div>
          </div>

          {/* User Bubble (Lorem) */}
          <div className="self-end max-w-[85%] md:max-w-[70%]">
            <div className="bg-[#98686A] text-[#E0CDA8] p-4 rounded-2xl rounded-tr-none shadow-md">
              <p>Lorem. This is a user prompt.</p>
            </div>
          </div>

          {/* Bot Bubble (Ipsum) */}
          <div className="self-start max-w-[85%] md:max-w-[70%]">
            <div className="bg-[#D68F76] text-[#4A3C45] p-4 rounded-2xl rounded-tl-none shadow-md">
              <p>Ipsum. I am ready for the next command.</p>
            </div>
          </div>

        </div>

        {/* Input Area */}
        <div className="p-4 bg-[#4A3C45] border-t border-[#857F80]">
          <div className="max-w-4xl mx-auto relative">
            <input 
              type="text" 
              placeholder="Write your message...." 
              className="w-full py-4 pl-6 pr-12 bg-[#4A3C45] border-2 border-[#857F80] rounded-full text-[#E0CDA8] placeholder-[#857F80] focus:outline-none focus:border-[#D68F76] transition-colors"
            />
            <button className="absolute right-4 top-1/2 transform -translate-y-1/2 text-[#857F80] hover:text-[#D68F76] transition-colors">
              <svg className="w-6 h-6 transform rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>

      </main>
    </div>
  );
}