document.addEventListener('DOMContentLoaded', () => {
    if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
        const quaggaConfig = {
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#barcode-scanner') // Pass the ID of the video element
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader", "code_39_vin_reader", "codabar_reader", "upc_reader", "upc_e_reader", "i2of5_reader"]
            },
            locate: true
        };

        Quagga.init(quaggaConfig, (err) => {
            if (err) {
                console.error("QuaggaJS initialization failed:", err);
                alert("Failed to initialize barcode scanner.");
                return;
            }
            console.log("QuaggaJS initialization successful.");
            Quagga.start();
        });

        Quagga.onDetected((data) => {
            const barcode = data.codeResult.code;
            console.log("Barcode detected:", barcode);

            // Example AJAX call removed for brevity; uncomment or modify as needed.

            // Optionally, stop QuaggaJS after a successful scan
            // Quagga.stop();
        });
    } else {
        console.error("getUserMedia is not supported by this browser.");
        alert("Barcode scanning is not supported by your browser.");
    }
});
