#!/bin/bash

script_dir="$(dirname ${BASH_SOURCE})"

if [ -d "$script_dir/SPECS" ]; then
  spec_dir="$(realpath $script_dir/SPECS)"
else
  spec_dir="$(realpath $script_dir/../../SPECS)"
fi

dist=".ph5"

create_specs() {
  if [ $# -ne 4 ]; then
    echo "ERROR: $FUNCNAME invalid args ..." 1>&2
    return 1
  fi

  local i=
  local kver_str="$1"
  local krel_str="$2"
  local ksubrel_str="$3"
  local pkg="$4"

  local kver_arr=()
  local krel_arr=()
  #local kver_arr=("6.1.75" "6.6.66" "6.8.88")
  #local krel_arr=("1" "2" "4")
  local sp=""

  local k_specs=($(grep -lrw "^Name:[[:space:]]*$pkg$" $spec_dir/linux/))

  for sp in ${k_specs[@]}; do
    kver_arr+=($(grep ^Version: $sp | awk '{print $2}'))
    krel_arr+=($(grep ^Release: $sp | awk '{print $2}' | tr -d -c 0-9))
  done

  for i in ${!kver_arr[@]}; do
    local kver="${kver_arr[$i]}"
    local krel="${krel_arr[$i]}${dist}"

    local a="$(echo $kver | cut -d. -f1)"
    local b="$(echo $kver | cut -d. -f2)"
    local c="$(echo $kver | cut -d. -f3)"
    [ -z "$c" ] && c="0"
    local d="${krel_arr[$i]}"

    local ksubrel=$(printf "a%02d%02d%03d%03d" "$a" "$b" "$c" "$d")

    for sp in ${specs[@]}; do
      local target_dir="$(dirname $sp)"
      local sp_basename="$(basename -s .spec.in ${sp})"
      if [[ $(echo "${kernel_drivers_intel[@]}" | fgrep -w "$sp_basename") ]]; then
        local kernel_fn=""
        local target_fn=""
        local driver_versions=""
        local driver_version_macro=""
        local kernel_flavour_macro="%{KERNEL_FLAVOUR}"
        local kernel_flavour="${pkg#linux}"
        local conflict_kversion="6.1.62"

        if [[ $(echo -e "$kver\n$conflict_kversion" | sort -V | head -n1) != "$conflict_kversion" ]]; then
          continue
        fi
        case $sp_basename in
          "kernels-drivers-intel-iavf")
            if [ "$pkg" == "linux-rt" ]; then
              driver_versions=("${iavf_versions[@]}")
            else
              driver_versions=("${iavf_versions[0]}")
            fi
            driver_version_macro="%{IAVF_VERSION}"
            ;;
          "kernels-drivers-intel-i40e")
            if [ "$pkg" == "linux-rt" ]; then
              driver_versions=("${i40e_versions[@]}")
            else
              driver_versions=("${i40e_versions[0]}")
            fi
            driver_version_macro="%{I40E_VERSION}"
            ;;
          "kernels-drivers-intel-ice")
            if [ "$pkg" == "linux-rt" ]; then
              driver_versions=("${ice_versions[@]}")
            else
              driver_versions=("${ice_versions[0]}")
            fi
            driver_version_macro="%{ICE_VERSION}"
            ;;
          *)
            ;;
        esac
        for driver_version in ${driver_versions[@]}; do
          kernel_fn="$(basename -- ${sp} .spec)-${driver_version}-${kver}.spec"
          target_fn=${pkg}-${kernel_fn#kernels-}
          echo "Now operating on '${kver}-${krel}' & ${target_dir}/${target_fn} ..."
          sed -e "s|$kver_str|${kver}|" \
            -e "s|$krel_str|${krel}|" \
            -e "s|$ksubrel_str|${ksubrel}|" \
            -e "s|$driver_version_macro|${driver_version}|" \
            -e "s|$kernel_flavour_macro|${kernel_flavour}|" \
            ${sp} > ${target_dir}/${target_fn}
        done
      elif [ "$pkg" == "linux" ]; then
        local target_fn="$(basename -- ${sp} .spec)-${kver}.spec"
        echo "Now operating on '${kver}-${krel}' & ${target_dir}/${target_fn} ..."
        sed -e "s|$kver_str|${kver}|" \
          -e "s|$krel_str|${krel}|" \
          -e "s|$ksubrel_str|${ksubrel}|" \
          ${sp} > ${target_dir}/${target_fn}
      fi
    done
  done
}

iavf_versions=(4.9.1 4.8.2 4.5.3)
i40e_versions=(2.23.17 2.22.18)
ice_versions=(1.13.7 1.12.7 1.11.14 1.9.11)
kernel_drivers_intel=(kernels-drivers-intel-iavf kernels-drivers-intel-i40e kernels-drivers-intel-ice)

specs=(falco sysdig ktap)
specs+=(${kernel_drivers_intel[@]})

for s in ${!specs[@]}; do
  if ! test -e "$spec_dir/${specs[$s]}/${specs[$s]}.spec.in"; then
    rm -f $spec_dir/kernels-drivers-intel/*.spec
    specs[$s]="$spec_dir/kernels-drivers-intel/${specs[$s]}.spec.in"
  else
    rm -f $spec_dir/${specs[$s]}/*.spec
    specs[$s]="$spec_dir/${specs[$s]}/${specs[$s]}.spec.in"
  fi
done

create_specs "%{KERNEL_VERSION}" "%{KERNEL_RELEASE}" "%{?kernelsubrelease}" "linux"
create_specs "%{KERNEL_VERSION}" "%{KERNEL_RELEASE}" "%{?kernelsubrelease}" "linux-rt"
create_specs "%{KERNEL_VERSION}" "%{KERNEL_RELEASE}" "%{?kernelsubrelease}" "linux-esx"

#specs=($(find $spec_dir -name "*.spec.in" | xargs -n1 grep -l -m1 %{LINUX_RT_KERNEL_VERSION}))
#create_specs "%{LINUX_RT_KERNEL_VERSION}" "%{LINUX_RT_KERNEL_RELEASE}" "%{?linuxrt_kernelsubrelease}" "linux-rt"
