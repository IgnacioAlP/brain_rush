document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-recompensa");
  const tabla = document.querySelector("#tabla-recompensas tbody");
  const idCuestionario = document.getElementById("id_cuestionario").value;
  const btnSubmit = form.querySelector('button[type="submit"]');
  const originalHTML = btnSubmit.innerHTML;
  let bloqueado = false; // 🔒 bandera lógica, no usa disabled real

  cargarRecompensas();

  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (bloqueado) return; // evita doble click
    bloqueado = true;

    // 🎨 estado visual “guardando”
    btnSubmit.classList.add("btn-secondary");
    btnSubmit.classList.remove("btn-warning");
    btnSubmit.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Guardando...`;

    const data = {
      nombre: form.nombre.value.trim(),
      descripcion: form.descripcion.value.trim(),
      puntos_requeridos: form.puntos.value.trim(),
      tipo: form.tipo.value.trim(),
      id_cuestionario: idCuestionario
    };

    try {
      const res = await fetch("/insertar_recompensa", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data)
      });

      const raw = await res.text();
      let result = {};
      try {
        result = JSON.parse(raw);
      } catch {
        console.warn("⚠️ Respuesta no JSON:", raw);
      }

      if (result.success) {
        mostrarToast("✅ Recompensa registrada con éxito", "success");

        // 🎉 feedback visual verde
        btnSubmit.classList.remove("btn-secondary");
        btnSubmit.classList.add("btn-success");
        btnSubmit.innerHTML = `<i class="fas fa-check"></i> Guardado`;

        form.reset();
        await cargarRecompensas();

        // 🔁 Restaurar en 1.2 s
        setTimeout(() => {
          btnSubmit.classList.remove("btn-success", "btn-secondary");
          btnSubmit.classList.add("btn-warning");
          btnSubmit.innerHTML = originalHTML;
          bloqueado = false;
        }, 1200);
      } else {
        mostrarToast("❌ Error al guardar recompensa", "danger");
        desbloquearBoton();
      }
    } catch (error) {
      console.error("❌ Error al insertar:", error);
      mostrarToast("⚠️ Error de conexión o formato inválido", "danger");
      desbloquearBoton();
    }
  });

  function desbloquearBoton() {
    setTimeout(() => {
      btnSubmit.classList.remove("btn-secondary", "btn-success");
      btnSubmit.classList.add("btn-warning");
      btnSubmit.innerHTML = originalHTML;
      bloqueado = false; // 🔓 libera bloqueo lógico
    }, 500);
  }

  async function cargarRecompensas() {
    try {
      const res = await fetch(`/recompensas_cuestionario/${idCuestionario}`);
      const data = await res.json();
      tabla.innerHTML = "";

      if (data.success && data.recompensas.length > 0) {
        data.recompensas.forEach(r => {
          const fila = document.createElement("tr");
          fila.innerHTML = `
            <td>${r.nombre}</td>
            <td>${r.descripcion || "—"}</td>
            <td>${r.puntos_requeridos}</td>
            <td>${r.tipo}</td>
            <td class="text-center">
              <button class="btn btn-sm btn-danger eliminar" data-id="${r.id_recompensa}">
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>`;
          tabla.appendChild(fila);
        });
      } else {
        tabla.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No hay recompensas registradas</td></tr>`;
      }
    } catch (error) {
      console.error("❌ Error al cargar recompensas:", error);
      tabla.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error al cargar recompensas</td></tr>`;
    }
  }

  tabla.addEventListener("click", async e => {
    if (e.target.closest(".eliminar")) {
      const id = e.target.closest(".eliminar").dataset.id;
      if (confirm("¿Eliminar esta recompensa?")) {
        try {
          const res = await fetch(`/eliminar_recompensa/${id}`, { method: "DELETE" });
          const data = await res.json();
          if (data.success) {
            mostrarToast("🗑️ Recompensa eliminada", "warning");
            await cargarRecompensas();
          } else {
            mostrarToast("❌ Error al eliminar", "danger");
          }
        } catch (error) {
          console.error("❌ Error al eliminar:", error);
          mostrarToast("⚠️ Fallo de conexión", "danger");
        }
      }
    }
  });

  function mostrarToast(mensaje, tipo = "info") {
    const toast = document.createElement("div");
    toast.className = `alert alert-${tipo} position-fixed bottom-0 end-0 m-3 shadow`;
    toast.style.zIndex = "2000";
    toast.textContent = mensaje;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
});
