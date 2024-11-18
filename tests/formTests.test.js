import { render, screen, fireEvent } from '@testing-library/dom';
import '@testing-library/jest-dom';  // Для зручних перевірок, як .toBeInTheDocument()

// Підключаємо JS файл
import '../static/recharge';

describe('Recharge Form', () => {
    beforeEach(() => {
        // Очищаємо перед кожним тестом
        document.body.innerHTML = `
            <form id="rechargeForm">
                <div class="input__group">
                    <label for="rechargeAmount">Wpisz kwotę, którą chcesz doładować.</label>
                    <input class="recharge__input" id="rechargeAmount" name="rechargeAmount" required />
                </div>
                <span class="error-message" id="errorMessage" role="alert"></span>
                <button type="submit" class="recharge__btn">Doładuj</button>
            </form>
        `;
    });

    test('shows error message when amount is empty', async () => {
        const amountInput = screen.getByLabelText(/Wpisz kwotę, którą chcesz doładować./i);
        const submitButton = screen.getByText(/Doładuj/i);
        const errorMessage = screen.getByRole('alert');  // використовуючи роль alert для отримання повідомлення

        // Тест на порожнє поле
        await fireEvent.click(submitButton);

        expect(errorMessage).toHaveTextContent(/Proszę wprowadzić prawidłową kwotę większą niż 0./i);
        expect(errorMessage).toBeInTheDocument();
    });

    test('shows error message for negative amount', async () => {
        const amountInput = screen.getByLabelText(/Wpisz kwotę, którą chcesz doładować./i);
        const submitButton = screen.getByText(/Doładuj/i);
        const errorMessage = screen.getByRole('alert');  // аналогічно, перевірка на помилку

        await fireEvent.change(amountInput, { target: { value: '-100' } });
        await fireEvent.click(submitButton);

        expect(errorMessage).toHaveTextContent(/Proszę wprowadzić prawidłową kwotę większą niż 0./i);
        expect(errorMessage).toBeInTheDocument();
    });

    test('does not show error message when amount is valid', async () => {
        const amountInput = screen.getByLabelText(/Wpisz kwotę, którą chcesz doładować./i);
        const submitButton = screen.getByText(/Doładuj/i);

        await fireEvent.change(amountInput, { target: { value: '100' } });
        await fireEvent.click(submitButton);

        // Очікуємо, що повідомлення про помилку не з'явиться
        const errorMessage = screen.queryByRole('alert');  // Використовуємо queryBy для перевірки, чи не існує елемент
        expect(errorMessage).not.toBeInTheDocument();
    });
});
