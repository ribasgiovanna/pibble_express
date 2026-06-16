function onlyNumbers(value) {
    return value.replace(/\D/g, "");
}

function maskCpf(value) {
    const numbers = onlyNumbers(value).slice(0, 11);
    return numbers
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

function maskCnpj(value) {
    const numbers = onlyNumbers(value).slice(0, 14);
    return numbers
        .replace(/(\d{2})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1/$2")
        .replace(/(\d{4})(\d{1,2})$/, "$1-$2");
}

function maskCpfCnpj(input) {
    const maxDigits = Number(input.dataset.maxDigits) || 14;
    const numbers = onlyNumbers(input.value).slice(0, maxDigits);
    const isCnpj = numbers.length > 11;

    input.value = isCnpj ? maskCnpj(numbers) : maskCpf(numbers);
    input.dataset.documentType = isCnpj ? "cnpj" : "cpf";
    input.removeAttribute("maxlength");
}

function limitDigits(input, value) {
    const maxDigits = Number(input.dataset.maxDigits);

    if (!maxDigits) {
        return value;
    }

    return onlyNumbers(value).slice(0, maxDigits);
}

function maskPhone(value) {
    const numbers = onlyNumbers(value).slice(0, 11);
    const mainNumberLength = numbers.length > 10 ? 5 : 4;
    const areaCode = numbers.slice(0, 2);
    const firstPart = numbers.slice(2, 2 + mainNumberLength);
    const secondPart = numbers.slice(2 + mainNumberLength);

    if (numbers.length <= 2) {
        return numbers;
    }

    if (!secondPart) {
        return `(${areaCode})${firstPart}`;
    }

    return `(${areaCode})${firstPart}-${secondPart}`;
}

function applyMask(input) {
    const mask = input.dataset.mask;

    if (mask === "cpf") {
        input.value = maskCpf(limitDigits(input, input.value));
    }

    if (mask === "cpf-cnpj") {
        maskCpfCnpj(input);
    }

    if (mask === "telefone") {
        input.value = maskPhone(limitDigits(input, input.value));
    }
}

document.querySelectorAll("[data-mask]").forEach((input) => {
    input.removeAttribute("maxlength");
    applyMask(input);
    input.addEventListener("input", () => applyMask(input));
});

document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    const input = button.closest(".password-field").querySelector("input");

    button.addEventListener("click", () => {
        const shouldShowPassword = input.type === "password";
        input.type = shouldShowPassword ? "text" : "password";
        button.setAttribute("aria-label", shouldShowPassword ? "Esconder senha" : "Mostrar senha");
        button.setAttribute("title", shouldShowPassword ? "Esconder senha" : "Mostrar senha");
    });
});
