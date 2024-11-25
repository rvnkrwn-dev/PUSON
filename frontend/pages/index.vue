<template>
  <!-- Breadcrumb -->
  <div
      class="sticky top-0 inset-x-0 z-20 bg-white border-y px-4 sm:px-6 lg:px-8 lg:hidden">
    <div class="flex items-center py-2">
      <!-- Navigation Toggle -->
      <button type="button"
              class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-none focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none"
              aria-haspopup="dialog" aria-expanded="false" aria-controls="hs-application-sidebar"
              aria-label="Toggle navigation" data-hs-overlay="#hs-application-sidebar">
        <span class="sr-only">Toggle Navigation</span>
        <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2"/>
          <path d="M15 3v18"/>
          <path d="m8 9 3 3-3 3"/>
        </svg>
      </button>
      <!-- End Navigation Toggle -->

      <!-- Breadcrumb -->
      <ol class="ms-3 flex items-center whitespace-nowrap">
        <li class="flex items-center text-sm text-gray-800">
          Aplikasi
          <svg class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400 " width="16"
               height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round"/>
          </svg>
        </li>
        <li class="text-sm font-semibold text-gray-800 truncate" aria-current="page">
          Dashboard
        </li>
      </ol>
      <!-- End Breadcrumb -->
    </div>
  </div>
  <!-- End Breadcrumb -->

  <!-- Content -->
  <div class="w-full lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
      <!-- Grid -->
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Puskesmas
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.puskesmas?.total }}
              </h3>
<!--              <span class="flex items-center gap-x-1 text-green-600">-->
<!--                <svg class="inline-block size-4 self-center" xmlns="http://www.w3.org/2000/svg" width="24" height="24"-->
<!--                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"-->
<!--                     stroke-linejoin="round">-->
<!--                  <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>-->
<!--                  <polyline points="16 7 22 7 22 13"/>-->
<!--                </svg>-->
<!--                <span class="inline-block text-sm">-->
<!--                  1.7%-->
<!--                </span>-->
<!--              </span>-->
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Posyandu
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.posyandu?.total }}
              </h3>
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Pengguna
              </p>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.user?.total }}
              </h3>
<!--              <span class="flex items-center gap-x-1 text-red-600">-->
<!--                <svg class="inline-block size-4 self-center" xmlns="http://www.w3.org/2000/svg" width="24" height="24"-->
<!--                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"-->
<!--                     stroke-linejoin="round">-->
<!--                  <polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/>-->
<!--                  <polyline points="16 17 22 17 22 11"/>-->
<!--                </svg>-->
<!--                <span class="inline-block text-sm">-->
<!--                  1.7%-->
<!--                </span>-->
<!--              </span>-->
            </div>
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div class="flex flex-col bg-white border shadow-sm rounded-xl">
          <div class="p-4 md:p-5">
            <div class="flex items-center gap-x-2">
              <p class="text-xs uppercase tracking-wide text-gray-500">
                Total Anak
              </p>
              <div class="hs-tooltip">
                <div class="hs-tooltip-toggle">
                  <svg class="shrink-0 size-4 text-gray-500" xmlns="http://www.w3.org/2000/svg"
                       width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <path d="M12 17h.01"/>
                  </svg>
                  <span
                      class="hs-tooltip-content hs-tooltip-shown:opacity-100 hs-tooltip-shown:visible opacity-0 transition-opacity inline-block absolute invisible z-10 py-1 px-2 bg-gray-900 text-xs font-medium text-white rounded shadow-sm"
                      role="tooltip">
                    {{ stats?.anak?.lakiLaki }} laki dan {{ stats?.anak?.perempuan }} perempuan
                  </span>
                </div>
              </div>
            </div>

            <div class="mt-1 flex items-center gap-x-2">
              <h3 class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.anak?.total }}
              </h3>
            </div>
          </div>
        </div>
        <!-- End Card -->
      </div>
      <!-- End Grid -->

      <div class="grid lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Card -->
        <div
            class="p-4 md:p-5 min-h-[410px] flex flex-col bg-white border shadow-sm rounded-xl">
          <!-- Header -->
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-sm text-gray-500">
                Stunting
              </h2>
              <p class="text-xl sm:text-2xl font-medium text-gray-800">
                30
              </p>
            </div>

            <div>
              <span
                  class="py-[5px] px-1.5 inline-flex items-center gap-x-1 text-xs font-medium rounded-md bg-teal-100 text-teal-800">
                <svg class="inline-block size-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                  <path d="M12 5v14"/>
                  <path d="m19 12-7 7-7-7"/>
                </svg>
                25%
              </span>
            </div>
          </div>
          <!-- End Header -->

          <div id="hs-multiple-bar-charts">
            <BarChart :series="dataOfAreaChart??[]" :categories="monthsOfAreaChart??[]" :color="['#3347ff', '#d333ff']" />
          </div>
        </div>
        <!-- End Card -->

        <!-- Card -->
        <div
            class="p-4 md:p-5 min-h-[410px] flex flex-col bg-white border shadow-sm rounded-xl">
          <!-- Header -->
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-sm text-gray-500">
                Anak
              </h2>
              <p class="text-xl sm:text-2xl font-medium text-gray-800">
                {{ stats?.anak?.total }}
              </p>
            </div>

            <div>
              <span
                  class="py-[5px] px-1.5 inline-flex items-center gap-x-1 text-xs font-medium rounded-md bg-red-100 text-red-800">
                <svg class="inline-block size-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                  <path d="M12 5v14"/>
                  <path d="m19 12-7 7-7-7"/>
                </svg>
                2%
              </span>
            </div>
          </div>
          <!-- End Header -->

          <div id="hs-single-area-chart">
            <AreaChart :series="dataOfAreaChart??[]" :categories="monthsOfAreaChart??[]" :color="['#3347ff', '#d333ff']" />
          </div>
        </div>
        <!-- End Card -->
      </div>

      <!-- Card -->
      <div class="flex flex-col">
        <div class="-m-1.5 overflow-x-auto">
          <div class="p-1.5 min-w-full inline-block align-middle">
            <div
                class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
              <!-- Header -->
              <div
                  class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-b border-gray-200">
                <div>
                  <h2 class="text-xl font-semibold text-gray-800">
                    Users
                  </h2>
                  <p class="text-sm text-gray-600">
                    Add users, edit and more.
                  </p>
                </div>

                <div>
                  <div class="inline-flex gap-x-2">
                    <a class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none focus:outline-none focus:bg-gray-50"
                       href="#">
                      View all
                    </a>

                    <a class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                       href="#">
                      <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                           stroke-linejoin="round">
                        <path d="M5 12h14"/>
                        <path d="M12 5v14"/>
                      </svg>
                      Add user
                    </a>
                  </div>
                </div>
              </div>
              <!-- End Header -->

              <!-- Table -->
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="ps-6 py-3 text-start">
                    <label for="hs-at-with-checkboxes-main" class="flex">
                      <input type="checkbox"
                             class="shrink-0 border-gray-300 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                             id="hs-at-with-checkboxes-main">
                      <span class="sr-only">Checkbox</span>
                    </label>
                  </th>

                  <th scope="col" class="ps-6 lg:ps-3 xl:ps-0 pe-6 py-3 text-start">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800">
                          Name
                        </span>
                    </div>
                  </th>

                  <th scope="col" class="px-6 py-3 text-start">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800">
                          Position
                        </span>
                    </div>
                  </th>

                  <th scope="col" class="px-6 py-3 text-start">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800">
                          Status
                        </span>
                    </div>
                  </th>

                  <th scope="col" class="px-6 py-3 text-start">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800">
                          Portfolio
                        </span>
                    </div>
                  </th>

                  <th scope="col" class="px-6 py-3 text-start">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800">
                          Created
                        </span>
                    </div>
                  </th>

                  <th scope="col" class="px-6 py-3 text-end"></th>
                </tr>
                </thead>

                <tbody class="divide-y divide-gray-200">
                <tr>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 py-3">
                      <label for="hs-at-with-checkboxes-1" class="flex">
                        <input type="checkbox"
                               class="shrink-0 border-gray-300 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                               id="hs-at-with-checkboxes-1">
                        <span class="sr-only">Checkbox</span>
                      </label>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 lg:ps-3 xl:ps-0 pe-6 py-3">
                      <div class="flex items-center gap-x-3">
                        <img class="inline-block size-[38px] rounded-full"
                             src="https://images.unsplash.com/photo-1531927557220-a9e23c1e4794?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=facearea&facepad=2&w=320&h=320&q=80"
                             alt="Avatar">
                        <div class="grow">
                          <span
                              class="block text-sm font-semibold text-gray-800">Christina Bersh</span>
                          <span class="block text-sm text-gray-500">christina@site.com</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="h-px w-72 whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="block text-sm font-semibold text-gray-800">Director</span>
                      <span class="block text-sm text-gray-500">Human resources</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                        <span
                            class="py-1 px-1.5 inline-flex items-center gap-x-1 text-xs font-medium bg-teal-100 text-teal-800 rounded-full">
                          <svg class="size-2.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                               fill="currentColor" viewBox="0 0 16 16">
                            <path
                                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                          </svg>
                          Active
                        </span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <div class="flex items-center gap-x-3">
                        <span class="text-xs text-gray-500">1/5</span>
                        <div class="flex w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div class="flex flex-col justify-center overflow-hidden bg-gray-800"
                               role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0"
                               aria-valuemax="100"></div>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="text-sm text-gray-500">28 Dec, 12:12</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-1.5">
                      <a class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                         href="#">
                        Edit
                      </a>
                    </div>
                  </td>
                </tr>

                <tr>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 py-3">
                      <label for="hs-at-with-checkboxes-2" class="flex">
                        <input type="checkbox"
                               class="shrink-0 border-gray-300 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                               id="hs-at-with-checkboxes-2">
                        <span class="sr-only">Checkbox</span>
                      </label>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 lg:ps-3 xl:ps-0 pe-6 py-3">
                      <div class="flex items-center gap-x-3">
                        <img class="inline-block size-[38px] rounded-full"
                             src="https://images.unsplash.com/photo-1568602471122-7832951cc4c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=facearea&facepad=2&w=320&h=320&q=80"
                             alt="Avatar">
                        <div class="grow">
                          <span
                              class="block text-sm font-semibold text-gray-800">David Harrison</span>
                          <span class="block text-sm text-gray-500">david@site.com</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="h-px w-72 whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="block text-sm font-semibold text-gray-800">Seller</span>
                      <span class="block text-sm text-gray-500">Branding products</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                        <span
                            class="py-1 px-1.5 inline-flex items-center gap-x-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">
                          <svg class="size-2.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                               fill="currentColor" viewBox="0 0 16 16">
                            <path
                                d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                          </svg>
                          Warning
                        </span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <div class="flex items-center gap-x-3">
                        <span class="text-xs text-gray-500">3/5</span>
                        <div class="flex w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div class="flex flex-col justify-center overflow-hidden bg-gray-800"
                               role="progressbar" style="width: 78%" aria-valuenow="78" aria-valuemin="0"
                               aria-valuemax="100"></div>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="text-sm text-gray-500">20 Dec, 09:27</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-1.5">
                      <a class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                         href="#">
                        Edit
                      </a>
                    </div>
                  </td>
                </tr>

                <tr>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 py-3">
                      <label for="hs-at-with-checkboxes-3" class="flex">
                        <input type="checkbox"
                               class="shrink-0 border-gray-300 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                               id="hs-at-with-checkboxes-3">
                        <span class="sr-only">Checkbox</span>
                      </label>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="ps-6 lg:ps-3 xl:ps-0 pe-6 py-3">
                      <div class="flex items-center gap-x-3">
                          <span
                              class="inline-flex items-center justify-center size-[38px] rounded-full bg-white border border-gray-300">
                            <span class="font-medium text-sm text-gray-800 leading-none">A</span>
                          </span>
                        <div class="grow">
                          <span
                              class="block text-sm font-semibold text-gray-800">Anne Richard</span>
                          <span class="block text-sm text-gray-500">anne@site.com</span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="h-px w-72 whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="block text-sm font-semibold text-gray-800">Designer</span>
                      <span class="block text-sm text-gray-500">IT department</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                        <span
                            class="py-1 px-1.5 inline-flex items-center gap-x-1 text-xs font-medium bg-teal-100 text-teal-800 rounded-full">
                          <svg class="size-2.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                               fill="currentColor" viewBox="0 0 16 16">
                            <path
                                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                          </svg>
                          Active
                        </span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <div class="flex items-center gap-x-3">
                        <span class="text-xs text-gray-500">5/5</span>
                        <div class="flex w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div class="flex flex-col justify-center overflow-hidden bg-gray-800"
                               role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0"
                               aria-valuemax="100"></div>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-3">
                      <span class="text-sm text-gray-500">18 Dec, 15:20</span>
                    </div>
                  </td>
                  <td class="size-px whitespace-nowrap">
                    <div class="px-6 py-1.5">
                      <a class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-none focus:underline font-medium"
                         href="#">
                        Edit
                      </a>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
              <!-- End Table -->

              <!-- Footer -->
              <div
                  class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-t border-gray-200">
                <div>
                  <p class="text-sm text-gray-600">
                    <span class="font-semibold text-gray-800">12</span> results
                  </p>
                </div>

                <div>
                  <div class="inline-flex gap-x-2">
                    <button type="button"
                            class="py-1.5 px-2 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none focus:outline-none focus:bg-gray-50">
                      <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                           stroke-linejoin="round">
                        <path d="m15 18-6-6 6-6"/>
                      </svg>
                      Prev
                    </button>

                    <button type="button"
                            class="py-1.5 px-2 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none focus:outline-none focus:bg-gray-50">
                      Next
                      <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                           stroke-linejoin="round">
                        <path d="m9 18 6-6-6-6"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <!-- End Footer -->
            </div>
          </div>
        </div>
      </div>
      <!-- End Card -->
    </div>
  </div>
</template>

<script setup lang="ts">
import Swal from 'sweetalert2'
import {sleep} from "@antfu/utils";
import BarChart from "~/components/chart/BarChart.vue";
import AreaChart from "~/components/chart/AreaChart.vue";

// config
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl;

const stats = ref({
  "anak": {
    "lakiLaki": 0,
    "perempuan": 0,
    "total": 0
  },
  "posyandu": {
    "total": 0
  },
  "puskesmas": {
    "total": 0
  },
  "user": {
    "total": 0
  }
});

const fetchStats = async () => {
  try {
    await sleep(2000)
    stats.value = await useFetchApi('https://puso-be.vercel.app/auth/stats/all-data')
  } catch (e) {
    await Swal.fire({
      position: "bottom-end",
      icon: "error",
      title: "Gagal memuat data statistik",
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  }
}

const monthsOfAreaChart = ref<string[]>([]);  // To store the months (bulan)
const dataOfAreaChart = ref<Array<{ name: string; data: number[] }>>([]);  // To store the series data (Laki-laki, Perempuan)

// Function to fetch and process the data
const fetchGraphAnak = async () => {
  try {
    await sleep(2000) // Menunggu beberapa detik untuk simulasi loading
    // Fetch data from the API
    const data = await useFetchApi(`${apiUrl}/auth/stats/grafik-anak`);

    // Initialize empty arrays for storing the processed data
    const lakiLakiData: number[] = [];
    const perempuanData: number[] = [];

    // Process the response data to fit the chart format
    data.forEach((item: { bulan: string, jumlah_laki_laki: number, jumlah_perempuan: number }) => {
      monthsOfAreaChart.value.push(item.bulan.slice(0, 3));  // Add month to categories
      lakiLakiData.push(item.jumlah_laki_laki);  // Add jumlah_laki_laki to the series data
      perempuanData.push(item.jumlah_perempuan);  // Add jumlah_perempuan to the series data
    });

    // Format chart data
    dataOfAreaChart.value = [
      { name: 'Laki-laki', data: lakiLakiData },
      { name: 'Perempuan', data: perempuanData }
    ];

  } catch (error) {
    console.error('Failed to fetch data:', error);
  }
}

onMounted(async () => {
  await fetchStats()
  await fetchGraphAnak()
})
</script>

<style scoped>

</style>