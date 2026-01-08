import { useState } from 'react';
import { ArrowLeft, User, BookOpen, Heart, Settings, Bell, CreditCard, LogOut, MapPin, Calendar, Clock, CheckCircle, AlertCircle, Lightbulb, TrendingUp } from 'lucide-react';
import type { CourseInterest } from '../App';

interface UserProfileProps {
  courseInterests: CourseInterest[];
  onNavigateToCourse: () => void;
}

type ProfileSection = 'interests' | 'enrolled' | 'settings' | 'notifications';

// Mock data para cursos disponíveis - deixando propositalmente limitado para mostrar recomendações
const COURSE_AVAILABILITY = {
  'Assistente de Design de Embalagens': {
    'Unidade A - Centro': {
      'Segunda-feira': {
        'Noite (18h às 22h)': { available: true, startDate: '2026-02-15', enrollDeadline: '2026-02-08' },
      },
    },
  },
};

interface SimilarCourse {
  name: string;
  code: string;
  unit: string;
  distance: string;
  day: string;
  shift: string;
  startDate: string;
  enrollDeadline: string;
  matchType: 'same-day-shift' | 'same-unit-different-time' | 'similar-course';
}

const getSimilarCourses = (interest: CourseInterest): SimilarCourse[] => {
  const selectedUnits = interest.selectedUnit.split(', ');
  const selectedDays = interest.selectedDay.split(', ');
  const selectedShifts = interest.selectedShift.split(', ');

  // Base de dados de cursos similares disponíveis
  const availableSimilarCourses: SimilarCourse[] = [
    {
      name: 'Design Gráfico Avançado',
      code: 'CL-003',
      unit: 'Unidade C - Zona Norte',
      distance: '3.5 km',
      day: 'Terça-feira',
      shift: 'Tarde (13h às 17h)',
      startDate: '2026-02-20',
      enrollDeadline: '2026-02-13',
      matchType: 'same-day-shift',
    },
    {
      name: 'Design de Produto e Embalagens',
      code: 'CL-005',
      unit: 'Unidade B - Zona Sul',
      distance: '2.8 km',
      day: 'Quarta-feira',
      shift: 'Noite (18h às 22h)',
      startDate: '2026-02-18',
      enrollDeadline: '2026-02-11',
      matchType: 'similar-course',
    },
    {
      name: 'Comunicação Visual para Embalagens',
      code: 'CL-007',
      unit: 'Unidade D - Zona Leste',
      distance: '4.2 km',
      day: 'Quinta-feira',
      shift: 'Tarde (13h às 17h)',
      startDate: '2026-02-25',
      enrollDeadline: '2026-02-18',
      matchType: 'similar-course',
    },
    {
      name: 'Design e Marketing de Produto',
      code: 'CL-009',
      unit: 'Unidade E - Zona Oeste',
      distance: '5.1 km',
      day: 'Sexta-feira',
      shift: 'Manhã (08h às 12h)',
      startDate: '2026-02-27',
      enrollDeadline: '2026-02-20',
      matchType: 'similar-course',
    },
    {
      name: 'Assistente de Design de Embalagens',
      code: 'CL-001B',
      unit: 'Unidade F - Regional 1',
      distance: '6.3 km',
      day: 'Sábado',
      shift: 'Manhã (08h às 12h)',
      startDate: '2026-03-01',
      enrollDeadline: '2026-02-22',
      matchType: 'same-day-shift',
    },
  ];

  // Primeiro, tenta encontrar cursos que correspondem ao dia E turno
  let recommendations = availableSimilarCourses.filter(course => {
    const matchesDay = selectedDays.includes(course.day);
    const matchesShift = selectedShifts.includes(course.shift);
    return matchesDay && matchesShift;
  });

  // Se não encontrou, tenta encontrar cursos que correspondem apenas ao turno
  if (recommendations.length === 0) {
    recommendations = availableSimilarCourses.filter(course => {
      return selectedShifts.includes(course.shift);
    });
  }

  // Se ainda não encontrou, tenta encontrar cursos que correspondem apenas ao dia
  if (recommendations.length === 0) {
    recommendations = availableSimilarCourses.filter(course => {
      return selectedDays.includes(course.day);
    });
  }

  // Se ainda não encontrou nada, retorna todos os cursos similares como última opção
  if (recommendations.length === 0) {
    recommendations = availableSimilarCourses;
  }

  // Retorna no máximo 2 recomendações
  return recommendations.slice(0, 2);
};

const checkCourseAvailability = (interest: CourseInterest) => {
  const selectedUnits = interest.selectedUnit.split(', ');
  const selectedDays = interest.selectedDay.split(', ');
  const selectedShifts = interest.selectedShift.split(', ');

  // Verifica se alguma combinação está disponível
  for (const unit of selectedUnits) {
    for (const day of selectedDays) {
      for (const shift of selectedShifts) {
        const courseData = COURSE_AVAILABILITY[interest.courseName as keyof typeof COURSE_AVAILABILITY];
        if (!courseData) continue;

        const unitData = courseData[unit as keyof typeof courseData];
        if (!unitData) continue;

        const dayData = unitData[day as keyof typeof unitData];
        if (!dayData) continue;

        const shiftData = dayData[shift as keyof typeof dayData];
        if (shiftData?.available) {
          return {
            available: true,
            unit,
            day,
            shift,
            startDate: shiftData.startDate,
            enrollDeadline: shiftData.enrollDeadline,
          };
        }
      }
    }
  }

  return { available: false };
};

export function UserProfile({ courseInterests, onNavigateToCourse }: UserProfileProps) {
  const [selectedSection, setSelectedSection] = useState<ProfileSection>('interests');

  return (
    <div className="min-h-screen bg-[#121212]">
      {/* Header */}
      <header className="bg-black text-white border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={onNavigateToCourse}
                className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="text-2xl font-bold text-[#1DB954]">EduPlatform</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium">João Silva</p>
                <p className="text-xs text-gray-400">joao.silva@email.com</p>
              </div>
              <div className="w-10 h-10 bg-[#1DB954] rounded-full flex items-center justify-center text-black font-bold">
                JS
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="md:col-span-1">
            <div className="bg-[#181818] rounded-lg border border-gray-800 overflow-hidden">
              <div className="p-4 bg-gradient-to-br from-[#1DB954] to-[#1ed760] text-black">
                <div className="w-16 h-16 bg-black rounded-full flex items-center justify-center mx-auto mb-3 text-2xl font-bold text-[#1DB954]">
                  JS
                </div>
                <h2 className="text-center font-bold">João Silva</h2>
                <p className="text-center text-xs text-black/70">Aluno</p>
              </div>

              <nav className="p-2">
                <button
                  onClick={() => setSelectedSection('interests')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    selectedSection === 'interests'
                      ? 'bg-[#1DB954] text-black font-medium'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <Heart className="w-5 h-5" />
                  <span>Cursos de Interesse</span>
                </button>

                <button
                  onClick={() => setSelectedSection('enrolled')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    selectedSection === 'enrolled'
                      ? 'bg-[#1DB954] text-black font-medium'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <BookOpen className="w-5 h-5" />
                  <span>Cursos Matriculados</span>
                </button>

                <button
                  onClick={() => setSelectedSection('notifications')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    selectedSection === 'notifications'
                      ? 'bg-[#1DB954] text-black font-medium'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <Bell className="w-5 h-5" />
                  <span>Notificações</span>
                  <span className="ml-auto bg-[#1DB954] text-black text-xs px-2 py-0.5 rounded-full font-bold">3</span>
                </button>

                <button
                  onClick={() => setSelectedSection('settings')}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    selectedSection === 'settings'
                      ? 'bg-[#1DB954] text-black font-medium'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <Settings className="w-5 h-5" />
                  <span>Configurações</span>
                </button>

                <div className="border-t border-gray-800 my-2" />

                <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors">
                  <CreditCard className="w-5 h-5" />
                  <span>Pagamentos</span>
                </button>

                <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-900/20 transition-colors">
                  <LogOut className="w-5 h-5" />
                  <span>Sair</span>
                </button>
              </nav>
            </div>
          </div>

          {/* Content Area */}
          <div className="md:col-span-3">
            {selectedSection === 'interests' && (
              <div>
                <div className="mb-6">
                  <h1 className="text-3xl mb-2 text-white">Seus Cursos de Interesse</h1>
                  <p className="text-gray-400">
                    Acompanhe a disponibilidade e receba recomendações personalizadas
                  </p>
                </div>

                {courseInterests.length === 0 ? (
                  <div className="bg-[#181818] rounded-lg border border-gray-800 p-12 text-center">
                    <Heart className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                    <h3 className="text-xl mb-2 text-white">Nenhum curso de interesse registrado</h3>
                    <p className="text-gray-400 mb-6">
                      Navegue pelos nossos cursos e registre seu interesse para ser notificado
                    </p>
                    <button
                      onClick={onNavigateToCourse}
                      className="bg-[#1DB954] hover:bg-[#1ed760] text-black font-medium px-6 py-3 rounded-full transition-colors"
                    >
                      Explorar Cursos
                    </button>
                  </div>
                ) : (
                  <div className="space-y-6">
                    {courseInterests.map((interest) => {
                      const availability = checkCourseAvailability(interest);
                      const similarCourses = !availability.available ? getSimilarCourses(interest) : [];
                      const firstUnit = interest.selectedUnit.split(', ')[0];

                      return (
                        <div key={interest.id} className="bg-[#181818] rounded-lg border border-gray-800 overflow-hidden">
                          {/* Course Header */}
                          <div className="p-6 border-b border-gray-800">
                            <div className="flex items-start justify-between mb-4">
                              <div className="flex-1">
                                <h3 className="text-xl text-white mb-1">{interest.courseName}</h3>
                                <p className="text-sm text-gray-500">Código: CL-001</p>
                              </div>
                              <button className="text-gray-500 hover:text-white">
                                <X className="w-5 h-5" />
                              </button>
                            </div>

                            <div className="flex flex-wrap gap-3 text-sm">
                              <div className="flex items-center gap-1.5 text-gray-400">
                                <MapPin className="w-4 h-4 text-[#1DB954]" />
                                <span>{interest.selectedUnit.split(', ')[0]}{interest.selectedUnit.split(', ').length > 1 && ` +${interest.selectedUnit.split(', ').length - 1}`}</span>
                              </div>
                              <div className="flex items-center gap-1.5 text-gray-400">
                                <Calendar className="w-4 h-4 text-[#1DB954]" />
                                <span>{interest.selectedDay.split(', ')[0]}{interest.selectedDay.split(', ').length > 1 && ` +${interest.selectedDay.split(', ').length - 1}`}</span>
                              </div>
                              <div className="flex items-center gap-1.5 text-gray-400">
                                <Clock className="w-4 h-4 text-[#1DB954]" />
                                <span>{interest.selectedShift.split(', ')[0]}{interest.selectedShift.split(', ').length > 1 && ` +${interest.selectedShift.split(', ').length - 1}`}</span>
                              </div>
                            </div>
                          </div>

                          {/* Suas preferências */}
                          <div className="p-6 bg-[#1a1a1a] border-b border-gray-800">
                            <h4 className="text-sm font-medium text-gray-400 mb-3">Suas preferências:</h4>
                            <div className="flex flex-wrap gap-2">
                              {interest.selectedUnit.split(', ').slice(0, 3).map((unit, idx) => (
                                <span key={idx} className="inline-flex items-center gap-1.5 bg-[#121212] border border-gray-700 px-3 py-1.5 rounded-full text-sm">
                                  <MapPin className="w-3.5 h-3.5 text-[#1DB954]" />
                                  <span className="text-gray-300">{unit}</span>
                                </span>
                              ))}
                              {interest.selectedDay.split(', ').slice(0, 3).map((day, idx) => (
                                <span key={idx} className="inline-flex items-center gap-1.5 bg-[#121212] border border-gray-700 px-3 py-1.5 rounded-full text-sm">
                                  <Calendar className="w-3.5 h-3.5 text-[#1DB954]" />
                                  <span className="text-gray-300">{day}</span>
                                </span>
                              ))}
                              {interest.selectedShift.split(', ').slice(0, 2).map((shift, idx) => (
                                <span key={idx} className="inline-flex items-center gap-1.5 bg-[#121212] border border-gray-700 px-3 py-1.5 rounded-full text-sm">
                                  <Clock className="w-3.5 h-3.5 text-[#1DB954]" />
                                  <span className="text-gray-300">{shift}</span>
                                </span>
                              ))}
                            </div>
                          </div>

                          {/* Availability Status */}
                          <div className="p-6">
                            {availability.available ? (
                              <div className="bg-[#1DB954]/10 border border-[#1DB954] rounded-lg p-5">
                                <div className="flex items-start gap-3">
                                  <div className="flex-shrink-0 w-10 h-10 bg-[#1DB954] rounded-full flex items-center justify-center">
                                    <CheckCircle className="w-6 h-6 text-black" />
                                  </div>
                                  <div className="flex-1">
                                    <h4 className="font-bold text-[#1DB954] mb-2 text-lg flex items-center gap-2">
                                      🎉 Turma disponível!
                                    </h4>
                                    <p className="text-sm text-gray-300 mb-4">
                                      Encontramos uma turma que atende todos os seus critérios.
                                    </p>
                                    <div className="space-y-2 mb-4">
                                      <div className="flex items-center gap-2 text-sm">
                                        <MapPin className="w-4 h-4 text-[#1DB954]" />
                                        <span className="text-white font-medium">{availability.unit}</span>
                                      </div>
                                      <div className="flex items-center gap-2 text-sm">
                                        <Calendar className="w-4 h-4 text-[#1DB954]" />
                                        <span className="text-white font-medium">{availability.day} - {availability.shift}</span>
                                      </div>
                                      <div className="flex items-center gap-2 text-sm">
                                        <TrendingUp className="w-4 h-4 text-[#1DB954]" />
                                        <span className="text-white font-medium">
                                          Início: {new Date(availability.startDate).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })}
                                        </span>
                                      </div>
                                    </div>
                                    <div className="bg-[#1DB954]/20 border border-[#1DB954]/50 rounded-lg px-4 py-3 mb-4">
                                      <p className="text-sm text-[#1DB954] font-medium flex items-center gap-2">
                                        <AlertCircle className="w-4 h-4" />
                                        Matricule-se até {new Date(availability.enrollDeadline).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })}
                                      </p>
                                    </div>
                                    <button className="w-full bg-[#1DB954] hover:bg-[#1ed760] text-black font-bold py-3 rounded-full transition-colors">
                                      Realizar Matrícula
                                    </button>
                                  </div>
                                </div>
                              </div>
                            ) : (
                              <>
                                <div className="bg-orange-500/10 border border-orange-500 rounded-lg p-5 mb-6">
                                  <div className="flex items-start gap-3">
                                    <div className="flex-shrink-0 w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center">
                                      <AlertCircle className="w-6 h-6 text-black" />
                                    </div>
                                    <div className="flex-1">
                                      <h4 className="font-bold text-orange-400 mb-2">Curso indisponível</h4>
                                      <p className="text-sm text-gray-300">
                                        Não há turmas disponíveis em <strong className="text-orange-400">{firstUnit}</strong> nos dias e turno selecionados.
                                      </p>
                                    </div>
                                  </div>
                                </div>

                                {/* Similar Courses Recommendations - SEMPRE APARECE */}
                                {similarCourses.length > 0 && (
                                  <div className="bg-blue-500/5 border border-blue-500/30 rounded-lg p-6">
                                    <div className="flex items-center gap-2 mb-4">
                                      <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                                        <Lightbulb className="w-5 h-5 text-black" />
                                      </div>
                                      <h4 className="font-bold text-blue-400 text-lg">💡 Sugestão Personalizada</h4>
                                    </div>
                                    <p className="text-sm text-gray-400 mb-5">
                                      Encontramos {similarCourses.length > 1 ? 'cursos similares' : 'um curso similar'} em {similarCourses.length > 1 ? 'unidades próximas' : 'uma unidade próxima'}:
                                    </p>
                                    <div className="space-y-4">
                                      {similarCourses.map((course, idx) => (
                                        <div
                                          key={idx}
                                          className="bg-blue-500/10 border border-blue-500 rounded-lg p-5"
                                        >
                                          <div className="mb-4">
                                            <h5 className="font-bold text-white text-lg mb-1">{course.name}</h5>
                                            <p className="text-sm text-gray-400">Código: {course.code}</p>
                                          </div>
                                          <div className="space-y-2 mb-4">
                                            <div className="flex items-center gap-2 text-sm">
                                              <MapPin className="w-4 h-4 text-blue-400" />
                                              <span className="text-white font-medium">{course.unit}</span>
                                              <span className="text-gray-500">({course.distance} de distância)</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm">
                                              <Calendar className="w-4 h-4 text-blue-400" />
                                              <span className="text-white font-medium">{course.day} - {course.shift}</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm">
                                              <TrendingUp className="w-4 h-4 text-blue-400" />
                                              <span className="text-white font-medium">
                                                Início: {new Date(course.startDate).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })}
                                              </span>
                                            </div>
                                          </div>
                                          <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg px-4 py-3 mb-4">
                                            <p className="text-sm text-blue-400 font-medium flex items-center gap-2">
                                              <AlertCircle className="w-4 h-4" />
                                              Matricule-se até {new Date(course.enrollDeadline).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })}
                                            </p>
                                          </div>
                                          <div className="flex gap-3">
                                            <button className="flex-1 border-2 border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-black font-medium py-2.5 rounded-full transition-colors">
                                              Ver Detalhes
                                            </button>
                                            <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-black font-bold py-2.5 rounded-full transition-colors">
                                              Matricular
                                            </button>
                                          </div>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}

            {selectedSection === 'enrolled' && (
              <div>
                <div className="mb-6">
                  <h1 className="text-3xl mb-2 text-white">Cursos Matriculados</h1>
                  <p className="text-gray-400">Gerencie seus cursos ativos e histórico acadêmico</p>
                </div>
                <div className="bg-[#181818] rounded-lg border border-gray-800 p-12 text-center">
                  <BookOpen className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                  <h3 className="text-xl mb-2 text-white">Nenhum curso matriculado</h3>
                  <p className="text-gray-400">Você ainda não está matriculado em nenhum curso</p>
                </div>
              </div>
            )}

            {selectedSection === 'notifications' && (
              <div>
                <div className="mb-6">
                  <h1 className="text-3xl mb-2 text-white">Notificações</h1>
                  <p className="text-gray-400">Acompanhe as novidades sobre seus cursos</p>
                </div>
                <div className="space-y-3">
                  <div className="bg-blue-500/10 border border-blue-500 rounded-lg p-4">
                    <p className="font-medium text-blue-400">Nova turma disponível!</p>
                    <p className="text-sm text-gray-300 mt-1">
                      O curso "Assistente de Design de Embalagens" tem vagas abertas na Unidade A
                    </p>
                    <p className="text-xs text-gray-500 mt-2">Há 2 horas</p>
                  </div>
                  <div className="bg-[#181818] border border-gray-800 rounded-lg p-4">
                    <p className="font-medium text-white">Lembrete de pagamento</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Sua próxima mensalidade vence em 5 dias
                    </p>
                    <p className="text-xs text-gray-600 mt-2">Ontem</p>
                  </div>
                  <div className="bg-[#181818] border border-gray-800 rounded-lg p-4">
                    <p className="font-medium text-white">Bem-vindo à EduPlatform!</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Seu perfil foi criado com sucesso. Explore nossos cursos!
                    </p>
                    <p className="text-xs text-gray-600 mt-2">3 dias atrás</p>
                  </div>
                </div>
              </div>
            )}

            {selectedSection === 'settings' && (
              <div>
                <div className="mb-6">
                  <h1 className="text-3xl mb-2 text-white">Configurações de Perfil</h1>
                  <p className="text-gray-400">Gerencie suas informações pessoais e preferências</p>
                </div>
                <div className="bg-[#181818] rounded-lg border border-gray-800 p-6">
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">Nome Completo</label>
                      <input
                        type="text"
                        defaultValue="João Silva"
                        className="w-full px-4 py-3 bg-[#121212] border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-[#1DB954]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">Email</label>
                      <input
                        type="email"
                        defaultValue="joao.silva@email.com"
                        className="w-full px-4 py-3 bg-[#121212] border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-[#1DB954]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">Telefone</label>
                      <input
                        type="tel"
                        defaultValue="(11) 98765-4321"
                        className="w-full px-4 py-3 bg-[#121212] border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-[#1DB954]"
                      />
                    </div>
                    <button className="bg-[#1DB954] hover:bg-[#1ed760] text-black font-medium px-6 py-3 rounded-full transition-colors">
                      Salvar Alterações
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function X({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  );
}
