#include <iostream>

int main()
{
    setlocale(LC_ALL, "RU");

    int a, b;
    std::cout << "Введите два числа через пробел: ";
    std::cin >> a >> b;

    if (a < b) {
        a = a * 2;
    }

    std::cout << a << " — удвоенное число" << std::endl;
    std::cout << b << " — исходное число" << std::endl;

    // -----------------------------

    int x, y, z;
    std::cout << "\nВведите три числа через пробел: ";
    std::cin >> x >> y >> z;

    if (x > y && x > z)
        std::cout << x << " — самое большое" << std::endl;
    else if (y > x && y > z)
        std::cout << y << " — самое большое" << std::endl;
    else if (z > x && z > y)
        std::cout << z << " — самое большое" << std::endl;

    // -----------------------------

    int p, h, g;
    std::cout << "\nВведите три стороны треугольника: ";
    std::cin >> p >> h >> g;

    if (p <= 0 || h <= 0 || g <= 0)
        std::cout << "нет (стороны должны быть положительными)" << std::endl;
    else if (p + h <= g || p + g <= h || h + g <= p)
        std::cout << "нет (такой треугольник не существует)" << std::endl;
    else
        std::cout << "да (треугольник существует)" << std::endl;

    // -----------------------------

    int q;
    std::cout << "\nВведите четырёхзначное число: ";
    std::cin >> q;

    if (q < 1000)
        std::cout << "ЧИСЛО ДОЛЖНО БЫТЬ НЕ МЕНЬШЕ 1000" << std::endl;
    else if (q > 9999)
        std::cout << "ЧИСЛО ДОЛЖНО БЫТЬ НЕ БОЛЬШЕ 9999" << std::endl;
    else {
        int first = q / 1000;
        int second = (q / 100) % 10;
        int third = (q / 10) % 10;
        int fourth = q % 10;

        if (first + fourth == second - third)
            std::cout << "Соотношение верно" << std::endl;
        else
            std::cout << "Соотношение неверно" << std::endl;
    }

    // -----------------------------

    int d, s;
    std::cout << "\nВведите координаты точки (d, s): ";
    std::cin >> d >> s;

    if (d >= s && d < 3)
        std::cout << "Точка принадлежит области." << std::endl;
    else
        std::cout << "Точка не принадлежит области." << std::endl;

    return 0;
}
