// Safety factor calculation and display logic

function calculateSafetyFactor() {
    // Get input values
    const actualLevel = parseFloat(document.getElementById('actualWaterLevel').value);
    const criticalLevel = parseFloat(document.getElementById('criticalWaterLevel').value);
    
    // Validate inputs
    if (isNaN(actualLevel) || isNaN(criticalLevel)) {
        alert('Voer geldige waarden in voor beide stijghoogtes');
        return;
    }
    
    if (actualLevel <= 0 || criticalLevel <= 0) {
        alert('Stijghoogtes moeten positieve waarden zijn');
        return;
    }
    
    if (actualLevel > 100 || criticalLevel > 100) {
        alert('Stijghoogtes lijken onrealistisch hoog. Controleer de waarden.');
        return;
    }
    
    // Calculate safety factor (FS = Critical Level / Actual Level)
    const safetyFactor = criticalLevel / actualLevel;
    
    // Calculate safety margin
    const safetyMargin = criticalLevel - actualLevel;
    
    // Calculate target level (for FS = 1.10)
    const targetLevel = criticalLevel / 1.10;
    
    // Update display
    updateSafetyFactorDisplay(safetyFactor, actualLevel, criticalLevel, safetyMargin, targetLevel);
    
    // Show result section
    document.getElementById('resultSection').style.display = 'block';
    
    // Scroll to results
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

function updateSafetyFactorDisplay(fs, actualLevel, criticalLevel, safetyMargin, targetLevel) {
    // Update safety factor number
    document.getElementById('safetyFactorNumber').textContent = fs.toFixed(2);
    
    // Update detail values
    document.getElementById('displayActualLevel').textContent = actualLevel.toFixed(2) + ' m';
    document.getElementById('displayCriticalLevel').textContent = criticalLevel.toFixed(2) + ' m';
    document.getElementById('safetyMargin').textContent = safetyMargin.toFixed(2) + ' m';
    document.getElementById('targetLevel').textContent = targetLevel.toFixed(2) + ' m';
    
    // Determine safety status and apply styling
    const safetyDisplay = document.getElementById('safetyFactorDisplay');
    const statusMessage = document.getElementById('statusMessage');
    const statusTitle = document.getElementById('statusTitle');
    const statusDescription = document.getElementById('statusDescription');
    const recommendationText = document.getElementById('recommendationText');
    
    // Remove existing classes
    safetyDisplay.className = 'safety-factor-display';
    statusMessage.className = 'status-message';
    recommendationText.className = '';
    
    if (fs >= 1.10) {
        // SAFE - Green
        safetyDisplay.classList.add('safe');
        statusMessage.classList.add('safe');
        recommendationText.classList.add('safe');
        
        statusTitle.textContent = 'GEEN OPBARSTGEVAAR VERWACHT';
        statusDescription.textContent = 'De veiligheidsfactor is voldoende hoog. Het risico op opbarsten is minimaal.';
        
        recommendationText.innerHTML = `
            <strong>✓ Situatie is veilig</strong><br>
            • Huidige waterspanning is acceptabel<br>
            • Reguliere monitoring volstaat<br>
            • Geen directe maatregelen noodzakelijk
        `;
        
    } else if (fs >= 1.00) {
        // WARNING - Orange
        safetyDisplay.classList.add('warning');
        statusMessage.classList.add('warning');
        recommendationText.classList.add('warning');
        
        statusTitle.textContent = 'MOGELIJK OPBARSTGEVAAR';
        statusDescription.textContent = 'De veiligheidsfactor is laag. Verhoogde aandacht en monitoring zijn noodzakelijk.';
        
        recommendationText.innerHTML = `
            <strong>⚠ Verhoogde waakzaamheid vereist</strong><br>
            • Intensiveer monitoring van waterspanningen<br>
            • Overweeg preventieve maatregelen<br>
            • Streef naar stijghoogte onder ${targetLevel.toFixed(2)} m<br>
            • Raadpleeg specialist bij verdere stijging
        `;
        
    } else {
        // DANGER - Red
        safetyDisplay.classList.add('danger');
        statusMessage.classList.add('danger');
        recommendationText.classList.add('danger');
        
        statusTitle.textContent = 'OPBARSTGEVAAR!';
        statusDescription.textContent = 'KRITIEKE SITUATIE: De veiligheidsfactor is te laag. Onmiddellijke actie vereist!';
        
        recommendationText.innerHTML = `
            <strong>🚨 URGENT - Onmiddellijke actie vereist!</strong><br>
            • Stop alle activiteiten die waterspanning verhogen<br>
            • Implementeer direct maatregelen om waterdruk te verlagen<br>
            • Verlaag stijghoogte naar maximaal ${targetLevel.toFixed(2)} m<br>
            • Waarschuw alle betrokkenen<br>
            • Raadpleeg onmiddellijk een specialist<br>
            • Overweeg evacuatie van risicogebied
        `;
    }
}

// Add input validation and formatting
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove any non-numeric characters except decimal point
            this.value = this.value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
        });
        
        input.addEventListener('keypress', function(e) {
            // Allow Enter key to trigger calculation
            if (e.key === 'Enter') {
                calculateSafetyFactor();
            }
        });
    });
    
    // Auto-focus first input
    document.getElementById('actualWaterLevel').focus();
});

// Utility function to format numbers
function formatNumber(num, decimals = 2) {
    return num.toFixed(decimals).replace('.', ','); // Dutch decimal separator
}

// Add example data for testing
function loadExampleData(type) {
    const actualInput = document.getElementById('actualWaterLevel');
    const criticalInput = document.getElementById('criticalWaterLevel');
    
    switch(type) {
        case 'safe':
            actualInput.value = '10.50';
            criticalInput.value = '12.00';
            break;
        case 'warning':
            actualInput.value = '11.50';
            criticalInput.value = '12.00';
            break;
        case 'danger':
            actualInput.value = '12.50';
            criticalInput.value = '12.00';
            break;
    }
}