! Copyright (C) 2007 Nicole Riemer and Matthew West
! Licensed under the GNU General Public License version 2 or (at your
! option) any later version. See the file COPYING for details.
!
! Driver to compute equilibrium radius.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program equilib

  use pmc_inout
  use pmc_aero_data
  use pmc_env_state
  use pmc_util
  use pmc_condensation
  use pmc_aero_particle

  character(len=*), parameter :: aero_filename = "aerosol.dat"

  type(inout_file_t) :: file
  type(env_state_t) :: env_state
  type(aero_data_t) :: aero_data
  type(aero_particle_t) :: aero_particle
  character(len=300) :: tmp_str
  integer :: i

  ! read aerosol data
  call inout_open_read(aero_filename, file)
  call inout_read_aero_data(file, aero_data)
  call inout_close(file)
  call assert(624223346, aero_data%i_water > 0)

  ! check command line arguments
  if (iargc() .ne. (1 + aero_data%n_spec)) then
     write(6,*) 'Usage: partmc <temp> <RH> <species volumes>'
     write(6,'(a,i3,a)') 'Need ', (aero_data%n_spec - 1), ' species volumes'
     call exit(2)
  end if
  
  ! get and check commandline arguments
  call getarg(1, tmp_str)
  env_state%temp = string_to_real(tmp_str)

  call getarg(2, tmp_str)
  env_state%rel_humid = string_to_real(tmp_str)

  call aero_particle_alloc(aero_particle, aero_data%n_spec)
  do i = 2,aero_data%n_spec
     call getarg(i + 1, tmp_str)
     aero_particle%vol(i) = string_to_real(tmp_str)
  end do

  ! do equilibriation
  call equilibriate_particle(env_state, aero_data, aero_particle)

  ! write results to stdout
  write(*,*) 'temp = ', env_state%temp, ' K'
  write(*,*) 'RH = ', env_state%rel_humid
  write(*,*) ''
  do i = 1,aero_data%n_spec
     write(*,*) aero_data%name(i), aero_particle%vol(i), ' m^{-3}'
  end do

  write(*,*) ''
  write(*,*) 'Equilibrium water volume: ', &
       aero_particle%vol(aero_data%i_water), ' m^{-3}'
  write(*,*) 'Dry volume: ', aero_particle_volume(aero_particle) - &
       aero_particle%vol(aero_data%i_water), ' m^{-3}'
  write(*,*) 'Wet volume: ', aero_particle_volume(aero_particle), ' m^{-3}'

  call aero_particle_free(aero_particle)
  call aero_data_free(aero_data)
  call env_state_free(env_state)

end program equilib