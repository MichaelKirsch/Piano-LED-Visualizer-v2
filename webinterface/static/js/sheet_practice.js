(function () {
    'use strict';

    function getSheetWrapper() {
        return document.getElementById('sheet_wrapper');
    }

    function isSheetFullscreen() {
        var wrapper = getSheetWrapper();
        if (!wrapper) return false;
        var fs = document.fullscreenElement || document.webkitFullscreenElement ||
            document.mozFullScreenElement || document.msFullscreenElement;
        return fs === wrapper;
    }

    function updateFullscreenButton() {
        var enterIcon = document.getElementById('sheet_fullscreen_icon_enter');
        var exitIcon = document.getElementById('sheet_fullscreen_icon_exit');
        var btn = document.getElementById('sheet_fullscreen_btn');
        var label = btn ? btn.querySelector('span[data-translate="sheet_fullscreen"]') : null;
        var isFs = isSheetFullscreen();

        if (enterIcon) enterIcon.classList.toggle('hidden', isFs);
        if (exitIcon) exitIcon.classList.toggle('hidden', !isFs);
        if (label) {
            label.textContent = typeof translate === 'function'
                ? translate(isFs ? 'sheet_exit_fullscreen' : 'sheet_fullscreen')
                : (isFs ? 'Vollbild beenden' : 'Vollbild');
        }
    }

    function triggerSheetResize() {
        window.dispatchEvent(new Event('resize'));
        if (typeof window.alignCursor === 'function') {
            window.alignCursor(true);
        }
    }

    window.setSheetFollowScroll = function (enabled) {
        if (typeof opt !== 'undefined') {
            opt.followScore = enabled ? 1 : 0;
        }
    };

    window.toggleSheetFullscreen = function () {
        var wrapper = getSheetWrapper();
        if (!wrapper) return;

        if (isSheetFullscreen()) {
            var exitFs = document.exitFullscreen || document.webkitExitFullscreen ||
                document.mozCancelFullScreen || document.msExitFullscreen;
            if (exitFs) exitFs.call(document);
            return;
        }

        var reqFs = wrapper.requestFullscreen || wrapper.webkitRequestFullscreen ||
            wrapper.mozRequestFullScreen || wrapper.msRequestFullscreen;
        if (!reqFs) {
            wrapper.classList.add('sheet-fullscreen-fallback');
            updateFullscreenButton();
            triggerSheetResize();
            return;
        }

        var promise = reqFs.call(wrapper);
        if (promise && promise.then) {
            promise.then(function () {
                updateFullscreenButton();
                setTimeout(triggerSheetResize, 150);
            }).catch(function (err) {
                console.warn('Fullscreen not available:', err);
                wrapper.classList.add('sheet-fullscreen-fallback');
                updateFullscreenButton();
                triggerSheetResize();
            });
        }
    };

    function onFullscreenChange() {
        var wrapper = getSheetWrapper();
        if (!wrapper) return;

        if (!isSheetFullscreen()) {
            wrapper.classList.remove('sheet-fullscreen-fallback');
        }
        updateFullscreenButton();
        setTimeout(triggerSheetResize, 150);
    }

    ['fullscreenchange', 'webkitfullscreenchange', 'mozfullscreenchange', 'MSFullscreenChange']
        .forEach(function (event) {
            document.addEventListener(event, onFullscreenChange);
        });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isSheetFullscreen()) {
            setTimeout(updateFullscreenButton, 50);
        }
    });

    function isLocalDev() {
        return location.hostname === '127.0.0.1' || location.hostname === 'localhost';
    }

    function showDevControls() {
        if (!isLocalDev()) return;
        var demoBtn = document.getElementById('sheet_demo_btn');
        if (demoBtn) demoBtn.classList.add('visible');
    }

    window.startSheetDemoPlayback = function () {
        if (typeof window.go_to_time !== 'function') {
            console.warn('Sheet not loaded yet');
            return;
        }
        clearInterval(window._sheetDemoInterval);
        var t = 0;
        window._sheetDemoInterval = setInterval(function () {
            window.go_to_time(t);
            t += 0.4;
            if (t > 90) {
                clearInterval(window._sheetDemoInterval);
            }
        }, 400);
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', showDevControls);
    } else {
        showDevControls();
    }
})();
