@'
from pathlib import Path
import re

html_path = Path("F:/Nghịch Antigravity/cinematic_ocean_3d/index.html")
html_text = html_path.read_text(encoding="utf-8")

# 1. Add SVG Water Displacement Filter to HTML (right after <body>)
svg_filter = '''
  <!-- SVG Water Wave Undulation Filter -->
  <svg style="position: absolute; width: 0; height: 0; pointer-events: none;">
    <defs>
      <filter id="water-wave" x="-20%" y="-20%" width="140%" height="140%">
        <feTurbulence id="turbulence" type="fractalNoise" baseFrequency="0.012 0.008" numOctaves="2" result="warp" />
        <feDisplacementMap xChannelSelector="R" yChannelSelector="G" scale="22" in="SourceGraphic" in2="warp" />
      </filter>
    </defs>
  </svg>
  
  <!-- Canvas for Animated Marine Life (Turtles, Jellyfish, Fish Schools) -->
  <canvas id="marine-canvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 3; pointer-events: none;"></canvas>
'''

html_text = html_text.replace("<body>", "<body>\n" + svg_filter)

# 2. Update .bg-layer CSS to apply water wave and slow cinematic breathing
old_bg_css = """.bg-layer { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-size: cover; background-position: center; transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1), transform 1.2s cubic-bezier(0.16, 1, 0.3, 1); z-index: 0; opacity: 0; transform: scale(1.04); }
    .bg-layer.active { opacity: 1; transform: scale(1); }"""

new_bg_css = """.bg-layer { 
      position: fixed; 
      top: -5%; 
      left: -5%; 
      width: 110vw; 
      height: 110vh; 
      background-size: cover; 
      background-position: center; 
      transition: opacity 1.4s cubic-bezier(0.16, 1, 0.3, 1); 
      z-index: 0; 
      opacity: 0; 
      filter: url(#water-wave) brightness(0.95);
      animation: waterBreathe 18s ease-in-out infinite alternate;
    }
    .bg-layer.active { 
      opacity: 1; 
    }

    @keyframes waterBreathe {
      0% { transform: scale(1.02) translate(0px, 0px); }
      50% { transform: scale(1.07) translate(-15px, -10px); }
      100% { transform: scale(1.04) translate(10px, -20px); }
    }"""

html_text = html_text.replace(old_bg_css, new_bg_css)

# 3. Add Marine Life Animation Engine to Javascript
marine_js = '''
    // --- 4. Living Marine Life & Water Distortion Engine ---
    const marineCanvas = document.getElementById('marine-canvas');
    const mCtx = marineCanvas.getContext('2d');
    const turb = document.getElementById('turbulence');

    function resizeMarineCanvas() {
      marineCanvas.width = window.innerWidth;
      marineCanvas.height = window.innerHeight;
    }
    resizeMarineCanvas();
    window.addEventListener('resize', resizeMarineCanvas);

    // Dynamic SVG Wave Displacement (Simulating liquid undulation)
    let waveTime = 0;
    function animateWaterRipples() {
      waveTime += 0.008;
      if (turb) {
        const freqX = 0.01 + Math.sin(waveTime) * 0.003;
        const freqY = 0.008 + Math.cos(waveTime * 0.8) * 0.002;
        turb.setAttribute('baseFrequency', `${freqX.toFixed(5)} ${freqY.toFixed(5)}`);
      }
    }

    // --- Marine Creatures Simulation ---
    // 1. School of Fish (Sunlight Zone)
    const fishCount = 35;
    const fishSchool = [];
    for (let i = 0; i < fishCount; i++) {
      fishSchool.push({
        x: Math.random() * window.innerWidth,
        y: 80 + Math.random() * 250,
        speed: 1.5 + Math.random() * 1.8,
        length: 8 + Math.random() * 8,
        wiggle: Math.random() * Math.PI,
        opacity: 0.3 + Math.random() * 0.5
      });
    }

    // 2. Majestic Sea Turtle (Coral Zone)
    let turtle = {
      x: -120,
      y: window.innerHeight * 0.35,
      speed: 0.7,
      scale: 1,
      flipperAngle: 0,
      active: false
    };

    // 3. Bioluminescent Jellyfish (Abyss Zone)
    const jellyfishList = [];
    for (let i = 0; i < 7; i++) {
      jellyfishList.push({
        x: 100 + Math.random() * (window.innerWidth - 200),
        y: window.innerHeight + Math.random() * 300,
        speed: 0.4 + Math.random() * 0.5,
        radius: 22 + Math.random() * 18,
        pulse: Math.random() * Math.PI,
        glowColor: i % 2 === 0 ? 'rgba(56, 189, 248, ' : 'rgba(168, 85, 247, '
      });
    }

    function renderMarineLife() {
      mCtx.clearRect(0, 0, marineCanvas.width, marineCanvas.height);
      animateWaterRipples();

      const activeBg = document.querySelector('.bg-layer.active');
      const isSurface = activeBg && activeBg.id === 'bg-surface';
      const isCoral = activeBg && activeBg.id === 'bg-coral';
      const isAbyss = activeBg && activeBg.id === 'bg-abyss';

      // 1. Draw Fish (Surface Zone)
      if (isSurface) {
        mCtx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        for (let f of fishSchool) {
          f.x += f.speed;
          f.wiggle += 0.2;
          if (f.x > marineCanvas.width + 50) f.x = -50;

          mCtx.save();
          mCtx.translate(f.x, f.y + Math.sin(f.wiggle) * 3);
          mCtx.fillStyle = `rgba(224, 242, 254, ${f.opacity})`;
          mCtx.beginPath();
          mCtx.ellipse(0, 0, f.length, f.length * 0.35, 0, 0, Math.PI * 2);
          mCtx.fill();
          // Tail
          mCtx.beginPath();
          mCtx.moveTo(-f.length * 0.8, 0);
          mCtx.lineTo(-f.length * 1.3, -f.length * 0.35);
          mCtx.lineTo(-f.length * 1.3, f.length * 0.35);
          mCtx.closePath();
          mCtx.fill();
          mCtx.restore();
        }
      }

      // 2. Draw Sea Turtle (Coral Zone)
      if (isCoral) {
        turtle.x += turtle.speed;
        turtle.flipperAngle += 0.04;
        if (turtle.x > marineCanvas.width + 200) {
          turtle.x = -180;
          turtle.y = marineCanvas.height * (0.2 + Math.random() * 0.35);
        }

        mCtx.save();
        mCtx.translate(turtle.x, turtle.y + Math.sin(turtle.flipperAngle * 0.5) * 8);
        mCtx.fillStyle = 'rgba(16, 185, 129, 0.45)';
        mCtx.strokeStyle = 'rgba(52, 211, 153, 0.7)';
        mCtx.lineWidth = 2;

        // Shell
        mCtx.beginPath();
        mCtx.ellipse(0, 0, 45, 30, 0.1, 0, Math.PI * 2);
        mCtx.fill();
        mCtx.stroke();

        // Head
        mCtx.beginPath();
        mCtx.ellipse(48, -2, 14, 10, 0.1, 0, Math.PI * 2);
        mCtx.fill();
        mCtx.stroke();

        // Front Flippers (Moving)
        const flipperOffset = Math.sin(turtle.flipperAngle) * 15;
        mCtx.beginPath();
        mCtx.moveTo(25, -15);
        mCtx.quadraticCurveTo(45, -45 + flipperOffset, 15, -40 + flipperOffset);
        mCtx.closePath();
        mCtx.fill();

        mCtx.beginPath();
        mCtx.moveTo(25, 15);
        mCtx.quadraticCurveTo(45, 45 - flipperOffset, 15, 40 - flipperOffset);
        mCtx.closePath();
        mCtx.fill();

        mCtx.restore();
      }

      // 3. Draw Bioluminescent Jellyfish (Abyss Zone)
      if (isAbyss) {
        for (let j of jellyfishList) {
          j.pulse += 0.035;
          const expansion = Math.sin(j.pulse);
          j.y -= j.speed + (expansion > 0 ? expansion * 0.5 : 0);
          if (j.y < -120) {
            j.y = marineCanvas.height + 100;
            j.x = 80 + Math.random() * (marineCanvas.width - 160);
          }

          const curRadius = j.radius * (1 + expansion * 0.15);
          mCtx.save();
          mCtx.translate(j.x, j.y);

          // Glowing Bell
          const grad = mCtx.createRadialGradient(0, 0, 0, 0, 0, curRadius);
          grad.addColorStop(0, j.glowColor + '0.6)');
          grad.addColorStop(0.7, j.glowColor + '0.25)');
          grad.addColorStop(1, j.glowColor + '0)');

          mCtx.fillStyle = grad;
          mCtx.beginPath();
          mCtx.arc(0, 0, curRadius * 1.5, 0, Math.PI * 2);
          mCtx.fill();

          mCtx.fillStyle = j.glowColor + '0.45)';
          mCtx.strokeStyle = j.glowColor + '0.8)';
          mCtx.lineWidth = 1.5;
          mCtx.beginPath();
          mCtx.arc(0, 0, curRadius, Math.PI, 0);
          mCtx.closePath();
          mCtx.fill();
          mCtx.stroke();

          // Tentacles
          mCtx.strokeStyle = j.glowColor + '0.4)';
          mCtx.lineWidth = 1;
          for (let t = -curRadius * 0.6; t <= curRadius * 0.6; t += curRadius * 0.4) {
            mCtx.beginPath();
            mCtx.moveTo(t, 0);
            mCtx.bezierCurveTo(
              t + Math.sin(j.pulse + t) * 8, curRadius * 0.8,
              t - Math.cos(j.pulse) * 8, curRadius * 1.6,
              t, curRadius * 2.4
            );
            mCtx.stroke();
          }

          mCtx.restore();
        }
      }

      requestAnimationFrame(renderMarineLife);
    }
    renderMarineLife();
'''

html_text = html_text.replace("updateSlide(0);", marine_js + "\n    updateSlide(0);")

html_path.write_text(html_text, encoding="utf-8")
print("SUCCESSFULLY_ADDED_LIVING_WATER_AND_ANIMATED_CREATURES")
'@ | Out-File -FilePath "F:\Nghịch Antigravity\cinematic_ocean_3d\add_living_motion.py" -Encoding utf8
