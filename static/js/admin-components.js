/**
 * Admin Component Utilities for SI ESGP 1912 Same Manufahi
 * Theme colors and reusable component functions
 * Version: 1.0
 */

const AdminUI = {
    // Theme colors
    colors: {
        deepBlue: '#1B3A5C',
        primaryBlue: '#2563EB',
        blueHover: '#1D4ED8',
        goldAccent: '#D4952A',
        goldLight: '#F5C842',
        success: '#27ae60',
        danger: '#e74c3c',
        warning: '#D4952A',
        textPrimary: '#1F2937',
        textSecondary: '#6B7280',
        borderLight: '#E5E7EB',
        bgLight: '#F8F9FA'
    },

    /**
     * Initialize all components on page load
     */
    init() {
        this.initTooltips();
        this.initPopovers();
        this.initCarousels();
        // Note: DataTables initialization is handled by individual page templates
        // to allow for page-specific configurations. Call AdminUI.initDataTables()
        // manually if needed.
        // this.initDataTables();
        this.initDatePickers();
        this.initSelect2();
        console.log('Admin UI components initialized');
    },

    /**
     * Initialize Bootstrap tooltips
     */
    initTooltips() {
        if (typeof $ !== 'undefined' && $.fn.tooltip) {
            $('[data-toggle="tooltip"]').tooltip({
                trigger: 'hover',
                container: 'body'
            });
        }
    },

    /**
     * Initialize Bootstrap popovers
     */
    initPopovers() {
        if (typeof $ !== 'undefined' && $.fn.popover) {
            $('[data-toggle="popover"]').popover({
                trigger: 'focus',
                container: 'body',
                html: true
            });
        }
    },

    /**
     * Initialize carousels with custom settings
     */
    initCarousels() {
        if (typeof $ !== 'undefined' && $.fn.carousel) {
            $('.carousel').carousel({
                interval: 5000,
                pause: 'hover',
                wrap: true
            });
        }
    },

    /**
     * Initialize DataTables with theme colors
     */
    initDataTables() {
        if (typeof $ !== 'undefined' && $.fn.DataTable) {
            // Only initialize tables with .datatable class that haven't been initialized yet
            $('.datatable').each(function() {
                if (!$.fn.DataTable.isDataTable(this)) {
                    $(this).DataTable({
                        language: {
                            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-PT.json'
                        },
                        pageLength: 25,
                        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Hotu"]],
                        responsive: true,
                        autoWidth: false
                    });
                }
            });
        }
    },

    /**
     * Initialize date pickers
     */
    initDatePickers() {
        if (typeof $ !== 'undefined' && $.fn.datepicker) {
            $('.datepicker').datepicker({
                format: 'dd/mm/yyyy',
                autoclose: true,
                todayHighlight: true,
                language: 'pt'
            });
        }
    },

    /**
     * Initialize Select2 dropdowns
     */
    initSelect2() {
        if (typeof $ !== 'undefined' && $.fn.select2) {
            $('.select2').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
        }
    }
};

/**
 * Card management functions
 */
AdminUI.Card = {
    /**
     * Toggle card collapse
     * @param {string} cardId - Card element ID
     */
    toggle(cardId) {
        const card = $(`#${cardId}`);
        card.toggleClass('collapsed-card');
        card.find('.card-body').slideToggle(300);

        // Rotate icon
        const icon = card.find('.card-tools i.fa-minus, .card-tools i.fa-plus');
        icon.toggleClass('fa-minus fa-plus');
    },

    /**
     * Show loading state on card
     * @param {string} cardId - Card element ID
     */
    showLoading(cardId) {
        const card = $(`#${cardId}`);
        if (!card.find('.overlay').length) {
            card.addClass('overlay-wrapper');
            card.append(`
                <div class="overlay">
                    <i class="fas fa-sync fa-spin"></i>
                </div>
            `);
        }
    },

    /**
     * Hide loading state
     * @param {string} cardId - Card element ID
     */
    hideLoading(cardId) {
        const card = $(`#${cardId}`);
        card.find('.overlay').remove();
        card.removeClass('overlay-wrapper');
    },

    /**
     * Refresh card content via AJAX
     * @param {string} cardId - Card element ID
     * @param {string} url - AJAX URL
     * @param {function} callback - Success callback
     */
    refresh(cardId, url, callback) {
        this.showLoading(cardId);

        $.ajax({
            url: url,
            method: 'GET',
            success: (data) => {
                $(`#${cardId} .card-body`).html(data);
                this.hideLoading(cardId);
                if (callback) callback(data);
            },
            error: () => {
                this.hideLoading(cardId);
                AdminUI.Toast.error('Erro ao carregar dados');
            }
        });
    },

    /**
     * Create a new card dynamically
     * @param {object} options - Card configuration
     * @returns {string} HTML string
     */
    create(options) {
        const defaults = {
            id: 'card-' + Date.now(),
            title: 'Card Title',
            variant: 'primary',
            outline: false,
            collapsible: false,
            removable: false,
            body: '<p>Card content</p>',
            footer: null
        };

        const opts = { ...defaults, ...options };
        const cardClass = opts.outline ? `card-${opts.variant} card-outline` : `card-${opts.variant}`;

        let tools = '';
        if (opts.collapsible) {
            tools += '<button class="btn btn-tool" data-card-widget="collapse"><i class="fas fa-minus"></i></button>';
        }
        if (opts.removable) {
            tools += '<button class="btn btn-tool" data-card-widget="remove"><i class="fas fa-times"></i></button>';
        }

        let footer = opts.footer ? `<div class="card-footer">${opts.footer}</div>` : '';

        return `
            <div class="card ${cardClass}" id="${opts.id}">
                <div class="card-header">
                    <h3 class="card-title">${opts.title}</h3>
                    <div class="card-tools">${tools}</div>
                </div>
                <div class="card-body">${opts.body}</div>
                ${footer}
            </div>
        `;
    }
};

/**
 * Modal management functions
 */
AdminUI.Modal = {
    /**
     * Show a modal
     * @param {string} modalId - Modal element ID
     */
    show(modalId) {
        $(`#${modalId}`).modal('show');
    },

    /**
     * Hide a modal
     * @param {string} modalId - Modal element ID
     */
    hide(modalId) {
        $(`#${modalId}`).modal('hide');
    },

    /**
     * Create confirmation modal
     * @param {object} options - Modal configuration
     */
    confirm(options) {
        const defaults = {
            title: 'Konfirmasaun',
            message: 'Ita boot hakarak kontinua?',
            variant: 'danger',
            confirmText: 'Hakarak',
            cancelText: 'Kansela',
            onConfirm: () => {},
            onCancel: () => {}
        };

        const opts = { ...defaults, ...options };
        const modalId = 'modal-confirm-' + Date.now();

        const html = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header modal-${opts.variant}">
                            <h4 class="modal-title">${opts.title}</h4>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>${opts.message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">
                                ${opts.cancelText}
                            </button>
                            <button type="button" class="btn btn-${opts.variant}" id="${modalId}-confirm">
                                ${opts.confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        $('body').append(html);

        $(`#${modalId}-confirm`).on('click', function() {
            opts.onConfirm();
            $(`#${modalId}`).modal('hide');
        });

        $(`#${modalId}`).on('hidden.bs.modal', function() {
            $(this).remove();
        });

        $(`#${modalId}`).modal('show');
    },

    /**
     * Create a dynamic modal with AJAX content
     * @param {object} options - Modal configuration
     */
    ajax(options) {
        const defaults = {
            title: 'Modal',
            url: '',
            size: 'lg',
            onLoad: () => {},
            onError: () => {}
        };

        const opts = { ...defaults, ...options };
        const modalId = 'modal-ajax-' + Date.now();

        const html = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog modal-${opts.size}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h4 class="modal-title">${opts.title}</h4>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <div class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="sr-only">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        $('body').append(html);

        $.ajax({
            url: opts.url,
            method: 'GET',
            success: (data) => {
                $(`#${modalId} .modal-body`).html(data);
                opts.onLoad(data);
            },
            error: () => {
                $(`#${modalId} .modal-body`).html(`
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i>
                        Erro ao carregar konteudo
                    </div>
                `);
                opts.onError();
            }
        });

        $(`#${modalId}`).on('hidden.bs.modal', function() {
            $(this).remove();
        });

        $(`#${modalId}`).modal('show');
    }
};

/**
 * Toast notification functions
 */
AdminUI.Toast = {
    /**
     * Initialize toast container
     */
    _initContainer() {
        if (!$('.toast-container').length) {
            $('body').append('<div class="toast-container"></div>');
        }
    },

    /**
     * Show a toast notification
     * @param {object} options - Toast configuration
     */
    show(options) {
        this._initContainer();

        const defaults = {
            title: 'Notifikasaun',
            message: '',
            variant: 'info',
            autohide: true,
            delay: 3000,
            icon: 'fa-info-circle'
        };

        const opts = { ...defaults, ...options };
        const toastId = 'toast-' + Date.now();

        const html = `
            <div class="toast toast-${opts.variant}" id="${toastId}" role="alert" data-autohide="${opts.autohide}" data-delay="${opts.delay}">
                <div class="toast-header">
                    <i class="fas ${opts.icon} mr-2"></i>
                    <strong class="mr-auto">${opts.title}</strong>
                    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast">
                        <span>&times;</span>
                    </button>
                </div>
                <div class="toast-body">${opts.message}</div>
            </div>
        `;

        $('.toast-container').append(html);
        $(`#${toastId}`).toast('show');

        $(`#${toastId}`).on('hidden.bs.toast', function() {
            $(this).remove();
        });
    },

    /**
     * Success toast shorthand
     */
    success(message, title = 'Susesu') {
        this.show({
            title: title,
            message: message,
            variant: 'success',
            icon: 'fa-check-circle'
        });
    },

    /**
     * Error toast shorthand
     */
    error(message, title = 'Erro') {
        this.show({
            title: title,
            message: message,
            variant: 'danger',
            icon: 'fa-exclamation-circle',
            autohide: false
        });
    },

    /**
     * Warning toast shorthand
     */
    warning(message, title = 'Atensaun') {
        this.show({
            title: title,
            message: message,
            variant: 'warning',
            icon: 'fa-exclamation-triangle'
        });
    },

    /**
     * Info toast shorthand
     */
    info(message, title = 'Informasaun') {
        this.show({
            title: title,
            message: message,
            variant: 'info',
            icon: 'fa-info-circle'
        });
    }
};

/**
 * Form utilities
 */
AdminUI.Form = {
    /**
     * Validate form fields
     * @param {string} formId - Form element ID
     * @returns {boolean}
     */
    validate(formId) {
        const form = $(`#${formId}`)[0];

        if (form.checkValidity() === false) {
            form.classList.add('was-validated');
            return false;
        }

        return true;
    },

    /**
     * Submit form with loading state
     * @param {string} formId - Form element ID
     * @param {object} options - Submit options
     */
    submit(formId, options) {
        const defaults = {
            method: 'POST',
            beforeSubmit: () => {},
            onSuccess: () => {},
            onError: () => {},
            showLoading: true
        };

        const opts = { ...defaults, ...options };
        const form = $(`#${formId}`);

        if (!this.validate(formId)) {
            return;
        }

        if (opts.showLoading) {
            this.setLoading(formId, true);
        }

        opts.beforeSubmit();

        $.ajax({
            url: form.attr('action'),
            method: opts.method,
            data: form.serialize(),
            success: (data) => {
                if (opts.showLoading) {
                    this.setLoading(formId, false);
                }
                opts.onSuccess(data);
                AdminUI.Toast.success('Dadus rai ho susesu');
            },
            error: (xhr) => {
                if (opts.showLoading) {
                    this.setLoading(formId, false);
                }
                opts.onError(xhr);
                AdminUI.Toast.error('Erro ao rai dadus');
            }
        });
    },

    /**
     * Set form loading state
     * @param {string} formId - Form element ID
     * @param {boolean} loading - Loading state
     */
    setLoading(formId, loading) {
        const form = $(`#${formId}`);
        const submitBtn = form.find('button[type="submit"]');

        if (loading) {
            submitBtn.prop('disabled', true);
            submitBtn.addClass('btn-loading');
            form.find('input, select, textarea').prop('disabled', true);
        } else {
            submitBtn.prop('disabled', false);
            submitBtn.removeClass('btn-loading');
            form.find('input, select, textarea').prop('disabled', false);
        }
    },

    /**
     * Reset form
     * @param {string} formId - Form element ID
     */
    reset(formId) {
        const form = $(`#${formId}`)[0];
        form.reset();
        form.classList.remove('was-validated');

        // Reset Select2
        $(`#${formId} .select2`).val(null).trigger('change');
    },

    /**
     * Show field error
     * @param {string} fieldName - Field name
     * @param {string} message - Error message
     */
    showFieldError(fieldName, message) {
        const field = $(`[name="${fieldName}"]`);
        field.addClass('is-invalid');

        let feedback = field.siblings('.invalid-feedback');
        if (!feedback.length) {
            field.after(`<div class="invalid-feedback">${message}</div>`);
        } else {
            feedback.text(message);
        }
    },

    /**
     * Clear all field errors
     * @param {string} formId - Form element ID
     */
    clearErrors(formId) {
        $(`#${formId} .is-invalid`).removeClass('is-invalid');
        $(`#${formId} .invalid-feedback`).remove();
    }
};

/**
 * Table utilities
 */
AdminUI.Table = {
    /**
     * Refresh DataTable
     * @param {string} tableId - Table element ID
     */
    refresh(tableId) {
        if ($.fn.DataTable) {
            const table = $(`#${tableId}`).DataTable();
            if (table && table.ajax) {
                table.ajax.reload(null, false);
            }
        }
    },

    /**
     * Export table to CSV
     * @param {string} tableId - Table element ID
     * @param {string} filename - Export filename
     */
    exportCSV(tableId, filename = 'export.csv') {
        const table = $(`#${tableId}`).DataTable();
        const data = table.buttons ? table.buttons.exportData() : null;

        if (!data) {
            console.error('Export requires DataTables Buttons extension');
            return;
        }

        let csv = '';

        // Headers
        csv += data.header.join(',') + '\n';

        // Rows
        data.body.forEach(row => {
            csv += row.join(',') + '\n';
        });

        // Download
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    },

    /**
     * Add row to table
     * @param {string} tableId - Table element ID
     * @param {array} rowData - Row data array
     */
    addRow(tableId, rowData) {
        $(`#${tableId}`).DataTable().row.add(rowData).draw();
    },

    /**
     * Delete row from table
     * @param {string} tableId - Table element ID
     * @param {number} rowIndex - Row index
     */
    deleteRow(tableId, rowIndex) {
        $(`#${tableId}`).DataTable().row(rowIndex).remove().draw();
    },

    /**
     * Highlight row temporarily
     * @param {string} tableId - Table element ID
     * @param {number} rowIndex - Row index
     */
    highlightRow(tableId, rowIndex) {
        const row = $(`#${tableId}`).DataTable().row(rowIndex).node();
        $(row).addClass('table-primary');

        setTimeout(() => {
            $(row).removeClass('table-primary');
        }, 2000);
    }
};

/**
 * Carousel utilities
 */
AdminUI.Carousel = {
    /**
     * Go to specific slide
     * @param {string} carouselId - Carousel element ID
     * @param {number} slideIndex - Slide index
     */
    goToSlide(carouselId, slideIndex) {
        $(`#${carouselId}`).carousel(slideIndex);
    },

    /**
     * Next slide
     * @param {string} carouselId - Carousel element ID
     */
    next(carouselId) {
        $(`#${carouselId}`).carousel('next');
    },

    /**
     * Previous slide
     * @param {string} carouselId - Carousel element ID
     */
    prev(carouselId) {
        $(`#${carouselId}`).carousel('prev');
    },

    /**
     * Pause carousel
     * @param {string} carouselId - Carousel element ID
     */
    pause(carouselId) {
        $(`#${carouselId}`).carousel('pause');
    },

    /**
     * Start carousel cycling
     * @param {string} carouselId - Carousel element ID
     */
    cycle(carouselId) {
        $(`#${carouselId}`).carousel('cycle');
    },

    /**
     * Create carousel dynamically
     * @param {object} options - Carousel configuration
     * @returns {string} HTML string
     */
    create(options) {
        const defaults = {
            id: 'carousel-' + Date.now(),
            items: [],
            indicators: true,
            controls: true,
            interval: 5000
        };

        const opts = { ...defaults, ...options };

        let indicators = '';
        if (opts.indicators) {
            indicators = '<ol class="carousel-indicators">';
            opts.items.forEach((_, index) => {
                const active = index === 0 ? 'class="active"' : '';
                indicators += `<li data-target="#${opts.id}" data-slide-to="${index}" ${active}></li>`;
            });
            indicators += '</ol>';
        }

        let slides = '<div class="carousel-inner">';
        opts.items.forEach((item, index) => {
            const active = index === 0 ? 'active' : '';
            slides += `
                <div class="carousel-item ${active}">
                    <img src="${item.image}" class="d-block w-100" alt="${item.alt || ''}">
                    ${item.caption ? `
                        <div class="carousel-caption d-none d-md-block">
                            <h5>${item.caption.title}</h5>
                            <p>${item.caption.text}</p>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        slides += '</div>';

        let controls = '';
        if (opts.controls) {
            controls = `
                <a class="carousel-control-prev" href="#${opts.id}" role="button" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </a>
                <a class="carousel-control-next" href="#${opts.id}" role="button" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </a>
            `;
        }

        return `
            <div id="${opts.id}" class="carousel slide" data-ride="carousel" data-interval="${opts.interval}">
                ${indicators}
                ${slides}
                ${controls}
            </div>
        `;
    }
};

/**
 * Loading utilities
 */
AdminUI.Loading = {
    /**
     * Show full page overlay
     * @param {string} message - Loading message
     */
    show(message = 'Loading...') {
        if (!$('.overlay-loader').length) {
            $('body').append(`
                <div class="overlay-loader">
                    <div class="text-center">
                        <div class="spinner-border text-primary mb-3" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                        <p class="text-white">${message}</p>
                    </div>
                </div>
            `);
        }
    },

    /**
     * Hide full page overlay
     */
    hide() {
        $('.overlay-loader').fadeOut(300, function() {
            $(this).remove();
        });
    }
};

/**
 * General utility functions
 */
AdminUI.Utils = {
    /**
     * Format number with thousand separators
     * @param {number} num - Number to format
     * @returns {string}
     */
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    /**
     * Truncate text
     * @param {string} text - Text to truncate
     * @param {number} length - Max length
     * @returns {string}
     */
    truncate(text, length = 50) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    },

    /**
     * Copy text to clipboard
     * @param {string} text - Text to copy
     */
    copyToClipboard(text) {
        // Use modern Clipboard API if available
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                AdminUI.Toast.success('Kopia ba clipboard');
            }).catch(() => {
                AdminUI.Toast.error('Erro ao kopia');
            });
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                AdminUI.Toast.success('Kopia ba clipboard');
            } catch (err) {
                AdminUI.Toast.error('Erro ao kopia');
            }
            document.body.removeChild(textarea);
        }
    },

    /**
     * Debounce function
     * @param {function} func - Function to debounce
     * @param {number} wait - Wait time in ms
     * @returns {function}
     */
    debounce(func, wait = 300) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Generate random ID
     * @returns {string}
     */
    generateId() {
        return 'id-' + Math.random().toString(36).substring(2, 11);
    },

    /**
     * Smooth scroll to element
     * @param {string} elementId - Element ID
     */
    scrollTo(elementId) {
        $('html, body').animate({
            scrollTop: $(`#${elementId}`).offset().top - 100
        }, 500);
    }
};

/**
 * Chart utilities using theme colors
 */
AdminUI.Chart = {
    /**
     * Get theme color array for charts
     * @param {number} count - Number of colors needed
     * @returns {array}
     */
    getColors(count = 5) {
        const colors = [
            AdminUI.colors.deepBlue,
            AdminUI.colors.primaryBlue,
            AdminUI.colors.goldAccent,
            AdminUI.colors.success,
            AdminUI.colors.textSecondary
        ];
        return colors.slice(0, count);
    },

    /**
     * Create pie/doughnut chart
     * @param {string} canvasId - Canvas element ID
     * @param {object} data - Chart data
     */
    createPie(canvasId, data) {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded');
            return;
        }

        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: data.colors || this.getColors(data.values.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 10
                    }
                }
            }
        });
    },

    /**
     * Create bar chart
     * @param {string} canvasId - Canvas element ID
     * @param {object} data - Chart data
     */
    createBar(canvasId, data) {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded');
            return;
        }

        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: data.label || 'Data',
                    data: data.values,
                    backgroundColor: data.color || AdminUI.colors.primaryBlue,
                    borderColor: data.color || AdminUI.colors.primaryBlue,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        });
    },

    /**
     * Create line chart
     * @param {string} canvasId - Canvas element ID
     * @param {object} data - Chart data
     */
    createLine(canvasId, data) {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded');
            return;
        }

        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: data.label || 'Data',
                    data: data.values,
                    borderColor: data.color || AdminUI.colors.primaryBlue,
                    backgroundColor: data.color ? data.color + '20' : AdminUI.colors.primaryBlue + '20',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
};

// Initialize when document is ready
$(document).ready(function() {
    AdminUI.init();
});

// Export to window for global access
window.AdminUI = AdminUI;
