import { useState } from 'react';
import { X, ChevronDown, MapPin, Calendar, Clock } from 'lucide-react';
import type { CourseInterest } from '../App';

interface InterestModalProps {
  onClose: () => void;
  onSubmit: (data: Omit<CourseInterest, 'id' | 'registeredDate'>) => void;
  courseName: string;
}

const UNITS = [
  'Unidade A - Centro',
  'Unidade B - Zona Sul',
  'Unidade C - Zona Norte',
  'Unidade D - Zona Leste',
  'Unidade E - Zona Oeste',
  'Unidade F - Regional 1',
  'Unidade G - Regional 2',
  'Unidade H - Regional 3',
];

const DAYS = [
  'Segunda-feira',
  'Terça-feira',
  'Quarta-feira',
  'Quinta-feira',
  'Sexta-feira',
  'Sábado',
  'Domingo',
];

const SHIFTS = [
  'Manhã (08h às 12h)',
  'Tarde (13h às 17h)',
  'Noite (18h às 22h)',
  'Integral (08h às 17h)',
];

export function InterestModal({ onClose, onSubmit, courseName }: InterestModalProps) {
  const [selectedUnits, setSelectedUnits] = useState<string[]>([]);
  const [selectedDays, setSelectedDays] = useState<string[]>([]);
  const [selectedShifts, setSelectedShifts] = useState<string[]>([]);
  const [showUnitDropdown, setShowUnitDropdown] = useState(false);
  const [showDayDropdown, setShowDayDropdown] = useState(false);
  const [showShiftDropdown, setShowShiftDropdown] = useState(false);

  const toggleUnit = (unit: string) => {
    setSelectedUnits(prev => 
      prev.includes(unit) ? prev.filter(u => u !== unit) : [...prev, unit]
    );
  };

  const toggleDay = (day: string) => {
    setSelectedDays(prev => 
      prev.includes(day) ? prev.filter(d => d !== day) : [...prev, day]
    );
  };

  const toggleShift = (shift: string) => {
    setSelectedShifts(prev => 
      prev.includes(shift) ? prev.filter(s => s !== shift) : [...prev, shift]
    );
  };

  const selectAllUnits = () => {
    setSelectedUnits(selectedUnits.length === UNITS.length ? [] : [...UNITS]);
  };

  const selectAllDays = () => {
    setSelectedDays(selectedDays.length === DAYS.length ? [] : [...DAYS]);
  };

  const selectAllShifts = () => {
    setSelectedShifts(selectedShifts.length === SHIFTS.length ? [] : [...SHIFTS]);
  };

  const handleSubmit = () => {
    if (selectedUnits.length > 0 && selectedDays.length > 0 && selectedShifts.length > 0) {
      onSubmit({
        courseName,
        selectedUnit: selectedUnits.join(', '),
        selectedDay: selectedDays.join(', '),
        selectedShift: selectedShifts.join(', '),
      });
    }
  };

  const isFormValid = selectedUnits.length > 0 && selectedDays.length > 0 && selectedShifts.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-[#181818] rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-800">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-[#1DB954] to-[#1ed760] text-black p-6 rounded-t-2xl">
          <button
            onClick={onClose}
            className="absolute right-4 top-4 p-2 hover:bg-black/20 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          <h2 className="text-2xl font-bold pr-8">Registro de Interesse</h2>
          <p className="text-black/80 mt-2">{courseName}</p>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          <p className="text-gray-400">
            Selecione suas preferências abaixo. Você pode escolher múltiplas opções para aumentar suas chances 
            de encontrar uma turma ideal.
          </p>

          {/* Unit Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-2 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-[#1DB954]" />
              Unidades de Preferência *
            </label>
            <div className="relative">
              <button
                onClick={() => setShowUnitDropdown(!showUnitDropdown)}
                className={`w-full px-4 py-3 border-2 rounded-lg text-left flex items-center justify-between transition-colors ${
                  selectedUnits.length > 0
                    ? 'border-[#1DB954] bg-[#1DB954]/10' 
                    : 'border-gray-700 hover:border-gray-600 bg-[#121212]'
                }`}
              >
                <span className={selectedUnits.length > 0 ? 'text-white' : 'text-gray-500'}>
                  {selectedUnits.length > 0 
                    ? `${selectedUnits.length} unidade${selectedUnits.length > 1 ? 's' : ''} selecionada${selectedUnits.length > 1 ? 's' : ''}`
                    : 'Selecione uma ou mais unidades'}
                </span>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showUnitDropdown ? 'rotate-180' : ''}`} />
              </button>
              
              {showUnitDropdown && (
                <div className="absolute z-10 w-full mt-2 bg-[#282828] border-2 border-gray-700 rounded-lg shadow-xl max-h-64 overflow-y-auto">
                  <button
                    onClick={selectAllUnits}
                    className="w-full px-4 py-3 text-left bg-[#1DB954]/10 text-[#1DB954] font-medium hover:bg-[#1DB954]/20 transition-colors border-b border-gray-700"
                  >
                    {selectedUnits.length === UNITS.length ? '✓ Desmarcar Todas' : 'Selecionar Todas'}
                  </button>
                  {UNITS.map((unit) => (
                    <button
                      key={unit}
                      onClick={() => toggleUnit(unit)}
                      className={`w-full px-4 py-3 text-left hover:bg-[#1DB954]/10 transition-colors flex items-center gap-2 ${
                        selectedUnits.includes(unit) ? 'bg-[#1DB954]/20 text-[#1DB954]' : 'text-gray-300'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                        selectedUnits.includes(unit) ? 'bg-[#1DB954] border-[#1DB954]' : 'border-gray-600'
                      }`}>
                        {selectedUnits.includes(unit) && <span className="text-black text-xs">✓</span>}
                      </div>
                      {unit}
                    </button>
                  ))}
                </div>
              )}
            </div>
            {selectedUnits.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedUnits.map(unit => (
                  <span key={unit} className="bg-[#1DB954]/20 text-[#1DB954] px-3 py-1 rounded-full text-sm flex items-center gap-2">
                    {unit}
                    <button onClick={() => toggleUnit(unit)} className="hover:text-white">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Day Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-2 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-[#1DB954]" />
              Dias da Semana *
            </label>
            <div className="relative">
              <button
                onClick={() => setShowDayDropdown(!showDayDropdown)}
                className={`w-full px-4 py-3 border-2 rounded-lg text-left flex items-center justify-between transition-colors ${
                  selectedDays.length > 0
                    ? 'border-[#1DB954] bg-[#1DB954]/10' 
                    : 'border-gray-700 hover:border-gray-600 bg-[#121212]'
                }`}
              >
                <span className={selectedDays.length > 0 ? 'text-white' : 'text-gray-500'}>
                  {selectedDays.length > 0 
                    ? `${selectedDays.length} dia${selectedDays.length > 1 ? 's' : ''} selecionado${selectedDays.length > 1 ? 's' : ''}`
                    : 'Selecione um ou mais dias'}
                </span>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showDayDropdown ? 'rotate-180' : ''}`} />
              </button>
              
              {showDayDropdown && (
                <div className="absolute z-10 w-full mt-2 bg-[#282828] border-2 border-gray-700 rounded-lg shadow-xl">
                  <button
                    onClick={selectAllDays}
                    className="w-full px-4 py-3 text-left bg-[#1DB954]/10 text-[#1DB954] font-medium hover:bg-[#1DB954]/20 transition-colors border-b border-gray-700"
                  >
                    {selectedDays.length === DAYS.length ? '✓ Desmarcar Todos' : 'Selecionar Todos'}
                  </button>
                  {DAYS.map((day) => (
                    <button
                      key={day}
                      onClick={() => toggleDay(day)}
                      className={`w-full px-4 py-3 text-left hover:bg-[#1DB954]/10 transition-colors flex items-center gap-2 ${
                        selectedDays.includes(day) ? 'bg-[#1DB954]/20 text-[#1DB954]' : 'text-gray-300'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                        selectedDays.includes(day) ? 'bg-[#1DB954] border-[#1DB954]' : 'border-gray-600'
                      }`}>
                        {selectedDays.includes(day) && <span className="text-black text-xs">✓</span>}
                      </div>
                      {day}
                    </button>
                  ))}
                </div>
              )}
            </div>
            {selectedDays.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedDays.map(day => (
                  <span key={day} className="bg-[#1DB954]/20 text-[#1DB954] px-3 py-1 rounded-full text-sm flex items-center gap-2">
                    {day}
                    <button onClick={() => toggleDay(day)} className="hover:text-white">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Shift Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-2 flex items-center gap-2">
              <Clock className="w-4 h-4 text-[#1DB954]" />
              Turnos *
            </label>
            <div className="relative">
              <button
                onClick={() => setShowShiftDropdown(!showShiftDropdown)}
                className={`w-full px-4 py-3 border-2 rounded-lg text-left flex items-center justify-between transition-colors ${
                  selectedShifts.length > 0
                    ? 'border-[#1DB954] bg-[#1DB954]/10' 
                    : 'border-gray-700 hover:border-gray-600 bg-[#121212]'
                }`}
              >
                <span className={selectedShifts.length > 0 ? 'text-white' : 'text-gray-500'}>
                  {selectedShifts.length > 0 
                    ? `${selectedShifts.length} turno${selectedShifts.length > 1 ? 's' : ''} selecionado${selectedShifts.length > 1 ? 's' : ''}`
                    : 'Selecione um ou mais turnos'}
                </span>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showShiftDropdown ? 'rotate-180' : ''}`} />
              </button>
              
              {showShiftDropdown && (
                <div className="absolute z-10 w-full mt-2 bg-[#282828] border-2 border-gray-700 rounded-lg shadow-xl">
                  <button
                    onClick={selectAllShifts}
                    className="w-full px-4 py-3 text-left bg-[#1DB954]/10 text-[#1DB954] font-medium hover:bg-[#1DB954]/20 transition-colors border-b border-gray-700"
                  >
                    {selectedShifts.length === SHIFTS.length ? '✓ Desmarcar Todos' : 'Selecionar Todos'}
                  </button>
                  {SHIFTS.map((shift) => (
                    <button
                      key={shift}
                      onClick={() => toggleShift(shift)}
                      className={`w-full px-4 py-3 text-left hover:bg-[#1DB954]/10 transition-colors flex items-center gap-2 ${
                        selectedShifts.includes(shift) ? 'bg-[#1DB954]/20 text-[#1DB954]' : 'text-gray-300'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                        selectedShifts.includes(shift) ? 'bg-[#1DB954] border-[#1DB954]' : 'border-gray-600'
                      }`}>
                        {selectedShifts.includes(shift) && <span className="text-black text-xs">✓</span>}
                      </div>
                      {shift}
                    </button>
                  ))}
                </div>
              )}
            </div>
            {selectedShifts.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedShifts.map(shift => (
                  <span key={shift} className="bg-[#1DB954]/20 text-[#1DB954] px-3 py-1 rounded-full text-sm flex items-center gap-2">
                    {shift}
                    <button onClick={() => toggleShift(shift)} className="hover:text-white">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Info Box */}
          <div className="bg-[#1DB954]/10 border-l-4 border-[#1DB954] p-4 rounded">
            <p className="text-sm text-gray-300">
              <strong className="text-[#1DB954]">Atenção:</strong> Este é um registro de interesse. 
              Você será notificado quando houver turmas disponíveis que correspondam às suas preferências.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-[#121212] p-6 rounded-b-2xl border-t border-gray-800 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 border-2 border-gray-700 text-gray-300 rounded-full hover:bg-gray-800 transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={handleSubmit}
            disabled={!isFormValid}
            className={`flex-1 px-6 py-3 rounded-full transition-colors font-medium ${
              isFormValid
                ? 'bg-[#1DB954] hover:bg-[#1ed760] text-black'
                : 'bg-gray-800 text-gray-600 cursor-not-allowed'
            }`}
          >
            Confirmar Interesse
          </button>
        </div>
      </div>
    </div>
  );
}
