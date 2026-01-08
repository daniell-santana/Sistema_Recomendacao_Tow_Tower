import { useState } from 'react';
import { User, Menu, Search, ChevronDown } from 'lucide-react';
import { InterestModal } from './InterestModal';
import type { CourseInterest } from '../App';

interface CoursePageProps {
  onRegisterInterest: (interest: Omit<CourseInterest, 'id' | 'registeredDate'>) => void;
  onNavigateToProfile: () => void;
  isLoggedIn: boolean;
  onLogin: () => void;
}

export function CoursePage({ onRegisterInterest, onNavigateToProfile, isLoggedIn, onLogin }: CoursePageProps) {
  const [showModal, setShowModal] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const handleRegisterClick = () => {
    if (!isLoggedIn) {
      onLogin();
    }
    setShowModal(true);
  };

  const handleSubmitInterest = (data: Omit<CourseInterest, 'id' | 'registeredDate'>) => {
    onRegisterInterest(data);
    setShowModal(false);
  };

  return (
    <div className="relative">
      {/* Header */}
      <header className="bg-[#121212] text-white">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <div className="text-2xl font-bold text-[#1DB954]">EduPlatform</div>
              <nav className="hidden md:flex items-center gap-6 text-sm">
                <a href="#" className="hover:text-[#1DB954] transition-colors">Cursos</a>
                <a href="#" className="hover:text-[#1DB954] transition-colors">Sobre</a>
                <a href="#" className="hover:text-[#1DB954] transition-colors">Unidades</a>
                <a href="#" className="hover:text-[#1DB954] transition-colors">Processo Seletivo</a>
              </nav>
            </div>
            <div className="flex items-center gap-4">
              <Search className="w-5 h-5 cursor-pointer hover:text-[#1DB954] transition-colors" />
              <button
                onClick={onNavigateToProfile}
                className="flex items-center gap-2 hover:text-[#1DB954] transition-colors"
              >
                <User className="w-5 h-5" />
                <span className="hidden md:inline text-sm">Meu Perfil</span>
              </button>
              <button 
                className="md:hidden"
                onClick={() => setShowMobileMenu(!showMobileMenu)}
              >
                <Menu className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="bg-[#181818] border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <a href="#" className="hover:text-[#1DB954] transition-colors">Início</a>
            <span>/</span>
            <a href="#" className="hover:text-[#1DB954] transition-colors">Cursos Livres</a>
            <span>/</span>
            <span className="text-white">Assistente de Design de Embalagens</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 bg-[#121212] min-h-screen">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Course Info */}
          <div className="md:col-span-2">
            <div className="mb-6">
              <span className="inline-block bg-[#1DB954] text-black text-xs font-medium px-3 py-1 rounded-full mb-4">
                Cursos Livres
              </span>
              <h1 className="text-3xl mb-4 text-white">Curso de Assistente de Design de Embalagens</h1>
              <p className="text-gray-400 mb-4">
                Desenvolva competências para atuar como assistente na criação de projetos de embalagens, 
                considerando aspectos técnicos, estéticos e de comunicação visual.
              </p>
            </div>

            {/* Course Image */}
            <div className="bg-gray-800 rounded-lg mb-8 overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80" 
                alt="Design de Embalagens"
                className="w-full h-64 object-cover"
              />
            </div>

            {/* Course Details */}
            <div className="space-y-6 text-white">
              <div>
                <h2 className="text-xl mb-3">Requisitos</h2>
                <ul className="list-disc list-inside text-gray-400 space-y-2">
                  <li>Idade mínima: 16 anos</li>
                  <li>Ensino Fundamental completo</li>
                  <li>Conhecimentos básicos de informática</li>
                </ul>
              </div>

              <div>
                <h2 className="text-xl mb-3">O que você vai aprender</h2>
                <ul className="list-disc list-inside text-gray-400 space-y-2">
                  <li>Fundamentos do design de embalagens</li>
                  <li>Técnicas de criação e desenvolvimento de projetos</li>
                  <li>Materiais e processos de produção</li>
                  <li>Sustentabilidade e inovação em embalagens</li>
                  <li>Software de design gráfico aplicado</li>
                </ul>
              </div>

              <div>
                <h2 className="text-xl mb-3">Informações do Curso</h2>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Carga horária:</span>
                    <p className="font-medium text-white">160 horas</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Modalidade:</span>
                    <p className="font-medium text-white">Presencial</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Tipo:</span>
                    <p className="font-medium text-white">Qualificação Profissional</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Certificação:</span>
                    <p className="font-medium text-white">Sim</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="md:col-span-1">
            <div className="bg-[#181818] border border-gray-800 rounded-lg p-6 sticky top-4">
              <div className="mb-6">
                <p className="text-gray-400 text-sm mb-2">Investimento a partir de:</p>
                <p className="text-3xl text-[#1DB954] mb-1">R$ 2.450,00</p>
                <p className="text-sm text-gray-500">ou 10x de R$ 245,00</p>
              </div>

              <button
                onClick={handleRegisterClick}
                className="w-full bg-[#1DB954] hover:bg-[#1ed760] text-black font-medium py-3 rounded-full mb-3 transition-colors"
              >
                Registro de Interesse
              </button>

              <button className="w-full border-2 border-[#1DB954] text-[#1DB954] hover:bg-[#1DB954] hover:text-black font-medium py-3 rounded-full transition-colors">
                Ver Turmas Disponíveis
              </button>

              <div className="mt-6 pt-6 border-t border-gray-800 space-y-3 text-sm">
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 rounded-full bg-[#1DB954] flex items-center justify-center text-black text-xs flex-shrink-0 mt-0.5">
                    ✓
                  </div>
                  <p className="text-gray-400">Certificado reconhecido no mercado</p>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 rounded-full bg-[#1DB954] flex items-center justify-center text-black text-xs flex-shrink-0 mt-0.5">
                    ✓
                  </div>
                  <p className="text-gray-400">Professores especializados</p>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 rounded-full bg-[#1DB954] flex items-center justify-center text-black text-xs flex-shrink-0 mt-0.5">
                    ✓
                  </div>
                  <p className="text-gray-400">Infraestrutura completa</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-black text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold mb-3 text-[#1DB954]">EduPlatform</h3>
              <p className="text-sm text-gray-400">
                Educação profissional de qualidade há mais de 20 anos.
              </p>
            </div>
            <div>
              <h3 className="font-bold mb-3">Links Úteis</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-[#1DB954] transition-colors">Cursos</a></li>
                <li><a href="#" className="hover:text-[#1DB954] transition-colors">Unidades</a></li>
                <li><a href="#" className="hover:text-[#1DB954] transition-colors">Contato</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-3">Contato</h3>
              <p className="text-sm text-gray-400">
                Tel: 0800 883 2000<br />
                atendimento@eduplatform.com.br
              </p>
            </div>
            <div>
              <h3 className="font-bold mb-3">Redes Sociais</h3>
              <div className="flex gap-3">
                <a href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#1DB954] hover:text-black transition-colors">f</a>
                <a href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#1DB954] hover:text-black transition-colors">in</a>
                <a href="#" className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#1DB954] hover:text-black transition-colors">ig</a>
              </div>
            </div>
          </div>
        </div>
      </footer>

      {/* Modal */}
      {showModal && (
        <InterestModal
          onClose={() => setShowModal(false)}
          onSubmit={handleSubmitInterest}
          courseName="Assistente de Design de Embalagens"
        />
      )}
    </div>
  );
}