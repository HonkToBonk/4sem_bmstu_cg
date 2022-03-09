#include "mainwindow.h"
#include "ui_mainwindow.h"

int is_in_border_flag = 1;
int is_solved_flag = 0;
int temp_index = 0, state = NO_STATE;
cords_t temp[SIZE];

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
  ui->setupUi(this);

  QLocale locales(QLocale::C);
  locales.setNumberOptions(QLocale::RejectGroupSeparator);
  auto val = new QDoubleValidator(-10000000, 10000000, 3, this);
  val->setLocale(locales);
  ui->xcord->setValidator(val);
  ui->ycord->setValidator(val);
  ui->num->setValidator(new QIntValidator());

  scene = new QGraphicsScene(0, 0, 578, 578, this);
  // scene->setSceneRect(0, 0, 578, 578);
  ui->graph->setScene(scene);
}

MainWindow::~MainWindow() {
  delete ui;
  delete scene;
}

void MainWindow::on_exit_triggered() { QApplication::quit(); }

void MainWindow::on_task_triggered() {
  QMessageBox msgbox;
  msgbox.setIcon(QMessageBox::Information);
  msgbox.setWindowTitle("Условие задачи");
  msgbox.setText(
      "Вариант №17\n\n"
      "Из заданного на плоскости множества точек выбрать три различные точки "
      "так, чтобы "
      "разность между площадью круга, ограниченного окружностью, проходящей "
      "через эти "
      "три точки, и площадью треугольника с вершинами в этих точках была "
      "минимальной.");
  msgbox.setDefaultButton(QMessageBox::Save);
  msgbox.exec();
}

void MainWindow::on_reference_triggered() {
  QMessageBox msgbox;
  msgbox.setIcon(QMessageBox::Information);
  msgbox.setWindowTitle("О программе");
  msgbox.setText("Лабораторная работа № 1 \n\"Геометрическая задача с "
                 "отображением результатов в графическом режиме\""
                 "\n\nВыполнил: \nстудент Хрюкин А.А. группы ИУ7-44Б"
                 "\nФевраль, 2022."
                 "\n\nИнформация для взаимодейсвтия с программой:"
                 "\n1) Координаты точек являются действительными числами (ввод "
                 "дробной части через точку \".\")"
                 "\n2) Минимальное число точек, которое нужно ввести для "
                 "работы программы - 3 штуки (для задания треугольника)"
                 "\n3) Для изменения координат уже введенной точки необходимо "
                 "ввести номер изменяемой точки, новые координаты и нажать "
                 "кнопку \"изменить\""
                 "\n4) Для удаления точки достаточно ввести её номер и нажать "
                 "кнопку \"удалить\""
                 "\n5) Для добавления новой точки необходимо ввести ее "
                 "координаты и нажать кнопку \"добавить\"");
  msgbox.setDefaultButton(QMessageBox::Save);
  msgbox.exec();
}

void MainWindow::on_addbutton_clicked() {
  double xbuf = ui->xcord->text().toDouble();
  double ybuf = ui->ycord->text().toDouble();

  ui->xcord->clear();
  ui->ycord->clear();
  ui->num->clear();

  ui->cordtable->insertRow(ui->cordtable->rowCount());
  ui->cordtable->setItem(ui->cordtable->rowCount() - 1, 0,
                         new QTableWidgetItem(QString::number(xbuf, 'f', 3)));
  ui->cordtable->setItem(ui->cordtable->rowCount() - 1, 1,
                         new QTableWidgetItem(QString::number(ybuf, 'f', 3)));
  redraw();

  state = ADD_STATE;
}

void MainWindow::on_change_clicked() {
  double xbuf = ui->xcord->text().toDouble();
  double ybuf = ui->ycord->text().toDouble();
  long num = ui->num->text().toLong();
  ui->xcord->clear();
  ui->ycord->clear();
  ui->num->clear();

  if (num <= 0 || num > ui->cordtable->rowCount())
    MainWindow::msgbox_wrong_num();
  else {
    temp[temp_index].index = num;
    temp[temp_index].xc = ui->cordtable->item(num - 1, 0)->text().toDouble();
    temp[temp_index].yc = ui->cordtable->item(num - 1, 1)->text().toDouble();
    temp_index += 1;
    ui->cordtable->setItem(num - 1, 0,
                           new QTableWidgetItem(QString::number(xbuf, 'f', 3)));
    ui->cordtable->setItem(num - 1, 1,
                           new QTableWidgetItem(QString::number(ybuf, 'f', 3)));
    redraw();
  }

  state = CHANGE_STATE;
}

void MainWindow::msgbox_wrong_num() {
  QMessageBox msgbox;
  msgbox.setIcon(QMessageBox::Critical);
  msgbox.setWindowTitle("Ошибка ввода данных");
  msgbox.setText("Такого номера точки не существует, повторите ввод");
  msgbox.setDefaultButton(QMessageBox::Save);
  msgbox.exec();
}

void MainWindow::on_deletepointbutton_clicked() {
  long num = ui->num->text().toLong();
  ui->xcord->clear();
  ui->ycord->clear();
  ui->num->clear();

  if (num <= 0 || num > ui->cordtable->rowCount())
    MainWindow::msgbox_wrong_num();
  else {
    temp[temp_index].index = num;
    temp[temp_index].xc = ui->cordtable->item(num - 1, 0)->text().toDouble();
    temp[temp_index].yc = ui->cordtable->item(num - 1, 1)->text().toDouble();
    temp_index += 1;
    ui->cordtable->removeRow(num - 1);
    redraw();
  }

  state = DELETE_STATE;
}

void MainWindow::on_cordtable_itemSelectionChanged() {
  int row = ui->cordtable->currentRow();
  QString xbuf = ui->cordtable->item(row, 0)->text();
  QString ybuf = ui->cordtable->item(row, 1)->text();
  ui->xcord->setText(xbuf);
  ui->ycord->setText(ybuf);
  ui->num->setText(QString::number(row + 1));
}

void MainWindow::on_solve_clicked() {
  scene->clear();
  int rows = ui->cordtable->rowCount();
  if (rows < 3) {

    //Проверка ввода достаточного количества точек

    QMessageBox msgbox;
    msgbox.setIcon(QMessageBox::Critical);
    msgbox.setWindowTitle("Ошибка ввода данных");
    msgbox.setText("Для построения треугольника необходимо "
                   "ввести минимум 3 точки.");
    msgbox.setDefaultButton(QMessageBox::Save);
    msgbox.exec();
  } else {
    cords_t array[SIZE];
    cords_t answer[ANS], textanswer[ANS];
    center_t outcenter;
    double minsdiff;

    //Ввод данных
    for (int i = 0; i < rows; i++) {
      array[i].index = i;
      array[i].xc = ui->cordtable->item(i, 0)->text().toDouble();
      array[i].yc = ui->cordtable->item(i, 1)->text().toDouble();
    }
    textanswer[0].index = -1;

    //Обработка
    minsdiff = process(array, rows, textanswer);

    //Обработка ситуации вырожденного треугольника
    if (textanswer[0].index == -1) {
      QMessageBox msgbox;
      msgbox.setIcon(QMessageBox::Critical);
      msgbox.setWindowTitle("Ошибка обработки");
      msgbox.setText("Все треугольники вырожденные. \nРешение невозможно.");
      msgbox.setDefaultButton(QMessageBox::Save);
      msgbox.exec();
      return;
    }

    //Масштабирование координат найденного треугольника для лучшей отрисовки
    double xmin, xmax, ymin, ymax;
    maxcords(textanswer, &xmax, &ymax);
    mincords(textanswer, &xmin, &ymin);

    double kxmin = 0;
    double kxmax = ui->graph->width() - 40;
    double kymin = ui->graph->height() - 40;
    double kymax = 0;

    double kx = (kxmax - kxmin) / (xmax - xmin);
    double ky = (kymax - kymin) / (ymax - ymin);
    double k = std::min(fabs(kx), fabs(ky));
    ky *= -1;

    for (int i = 0; i < ANS; i++) {
      answer[i].xc = 20 + (textanswer[i].xc - xmin) * k * kx / fabs(kx);
      answer[i].yc = 20 + (ymax - textanswer[i].yc) * k * ky / fabs(ky);
    }

    //Вычисление параметров окружности по найденному треугольнику
    outside(answer, &outcenter);

    QPen triangle(Qt::red);
    QPen outcircle(Qt::blue);
    QPen points(Qt::green);
    QBrush fillpoints(Qt::green);
    triangle.setWidth(3);
    outcircle.setWidth(3);
    points.setWidth(3);

    scene->clear();
    delete scene;
    scene = new QGraphicsScene(this);
    ui->graph->setScene(scene);

    //Построение

    //Стороны треугольника
    scene->addLine(answer[0].xc, answer[0].yc, answer[1].xc, answer[1].yc,
                   triangle);
    scene->addLine(answer[1].xc, answer[1].yc, answer[2].xc, answer[2].yc,
                   triangle);
    scene->addLine(answer[2].xc, answer[2].yc, answer[0].xc, answer[0].yc,
                   triangle);

    //Описанная окружность
    scene->addEllipse(outcenter.xc - outcenter.rad,
                      outcenter.yc - outcenter.rad, 2 * outcenter.rad,
                      2 * outcenter.rad, outcircle);

    //Вершины треугольника
    scene->addEllipse(answer[0].xc - 4, answer[0].yc - 4, 8, 8, points,
                      fillpoints);
    scene->addEllipse(answer[1].xc - 4, answer[1].yc - 4, 8, 8, points,
                      fillpoints);
    scene->addEllipse(answer[2].xc - 4, answer[2].yc - 4, 8, 8, points,
                      fillpoints);

    //Подписи к вершинам треугольника
    QFont font = QFont("Times", 14, QFont::Bold);
    QGraphicsTextItem *first = scene->addText(QString("%1 (%2, %3)")
                                                  .arg(textanswer[0].index + 1)
                                                  .arg(textanswer[0].xc)
                                                  .arg(textanswer[0].yc),
                                              font);
    first->setPos(answer[0].xc, answer[0].yc);
    first->setDefaultTextColor(Qt::green);
    QGraphicsTextItem *second = scene->addText(QString("%1 (%2, %3)")
                                                   .arg(textanswer[1].index + 1)
                                                   .arg(textanswer[1].xc)
                                                   .arg(textanswer[1].yc),
                                               font);
    second->setPos(answer[1].xc, answer[1].yc);
    second->setDefaultTextColor(Qt::green);
    QGraphicsTextItem *third = scene->addText(QString("%1 (%2, %3)")
                                                  .arg(textanswer[2].index + 1)
                                                  .arg(textanswer[2].xc)
                                                  .arg(textanswer[2].yc),
                                              font);
    third->setPos(answer[2].xc, answer[2].yc);
    third->setDefaultTextColor(Qt::green);

    ui->graph->fitInView(ui->graph->sceneRect(), Qt::KeepAspectRatio);
    // graph->scene()->sceneRect(), Qt::KeepAspectRatio);
    scene->update();

    //Сообщение об успешном решении задачи
    QMessageBox msgbox;
    msgbox.setIcon(QMessageBox::Information);
    msgbox.setWindowTitle("Задача решена");
    msgbox.setText(
        QString("Треугольник был построен на точках №%1, №%2 и №%3.\n"
                "Разность площадей треугольника и описанной около него "
                "окружности составила dS = %4")
            .arg(textanswer[0].index + 1)
            .arg(textanswer[1].index + 1)
            .arg(textanswer[2].index + 1)
            .arg(minsdiff));
    msgbox.setDefaultButton(QMessageBox::Save);
    msgbox.exec();
    is_solved_flag = 1;
  }
}

void MainWindow::on_clear_clicked() {
  scene->clear();
  ui->xcord->clear();
  ui->ycord->clear();
  ui->num->clear();

  delete scene;
  scene = new QGraphicsScene(0, 0, 578, 578, this);
  // scene->setSceneRect(0, 0, 578, 578);
  if (is_solved_flag == 1)
    is_in_border_flag = 0;
  // ui->graph->fitInView(0, 0, 578, 578, Qt::KeepAspectRatio);
  ui->graph->setScene(scene);

  long n = ui->cordtable->rowCount();
  for (long i = n; i > 0; i--) {
    temp[i].xc = ui->cordtable->item(i - 1, 0)->text().toDouble();
    temp[i].yc = ui->cordtable->item(i - 1, 1)->text().toDouble();
    ui->cordtable->removeRow(i - 1);
  }
  temp_index = n;

  state = CLEAR_STATE;
}

void MainWindow::redraw() {
  QPen points(Qt::green);
  QBrush fillpoints(Qt::green);
  QFont font = QFont("Times", 14, QFont::Bold);
  cords_t pt[SIZE], to_redraw[SIZE];
  double xmin, xmax, ymin, ymax;
  int rows = ui->cordtable->rowCount();

  delete scene;
  scene = new QGraphicsScene(0, 0, 578, 578, this);
  // scene->setSceneRect(0, 0, 578, 578);
  ui->graph->setScene(scene);

  for (int i = 0; i < rows; i++) {
    pt[i].index = i;
    pt[i].xc = ui->cordtable->item(i, 0)->text().toDouble();
    pt[i].yc = ui->cordtable->item(i, 1)->text().toDouble();
    if (fabs(pt[i].xc) > 280 || fabs(pt[i].yc) > 280)
      is_in_border_flag = 0;
  }
  if (is_in_border_flag == 1) {
    for (int i = 0; i < rows; i++) {
      scene->addEllipse(pt[i].xc + 283 - 4, -1 * pt[i].yc + 286 - 4, 8, 8,
                        points, fillpoints);
      QGraphicsTextItem *num = scene->addText(QString("%1").arg(i + 1), font);
      num->setPos(pt[i].xc + 283, -1 * pt[i].yc + 286);
      num->setDefaultTextColor(Qt::green);
      scene->update();
    }
  } else {
    xmin = pt[0].xc - 1;
    ymin = pt[0].yc - 1;
    xmax = pt[0].xc;
    ymax = pt[0].yc;
    for (int i = 0; i < rows; i++) {
      if (pt[i].xc > xmax)
        xmax = (pt[i].xc);
      if (pt[i].yc > ymax)
        ymax = (pt[i].yc);
      if (pt[i].xc < xmin)
        xmin = (pt[i].xc);
      if (pt[i].yc < ymin)
        ymin = (pt[i].yc);
    }

    double kxmin = 0;
    double kxmax = ui->graph->width() - 40;
    double kymin = ui->graph->height() - 40;
    double kymax = 0;
    double kx = (kxmax - kxmin) / (xmax - xmin);
    double ky = (kymax - kymin) / (ymax - ymin);
    double k = std::min(fabs(kx), fabs(ky));
    ky *= -1;

    for (int i = 0; i < rows; i++) {
      to_redraw[i].xc = 20 + (pt[i].xc - xmin) * k * kx / fabs(kx);
      to_redraw[i].yc = 20 + (ymax - pt[i].yc) * k * ky / fabs(ky);
    }
    for (int i = 0; i < rows; i++) {
      scene->addEllipse(to_redraw[i].xc - 4, to_redraw[i].yc - 4, 8, 8, points,
                        fillpoints);
      QGraphicsTextItem *num = scene->addText(QString("%1").arg(i + 1), font);
      num->setPos(to_redraw[i].xc, to_redraw[i].yc);
      num->setDefaultTextColor(Qt::green);
    }
    if (rows >= 2)
      ui->graph->fitInView(ui->graph->scene()->sceneRect(),
                           Qt::KeepAspectRatio);
    scene->update();
  }
}

void MainWindow::mousePressEvent(QMouseEvent *e) {
  QPen points(Qt::green);
  QBrush fillpoints(Qt::green);
  QFont font = QFont("Times", 14, QFont::Bold);

  if (is_in_border_flag == 1) {
    QPointF pt = ui->graph->mapToScene(e->pos());
    ui->cordtable->insertRow(ui->cordtable->rowCount());
    ui->cordtable->setItem(
        ui->cordtable->rowCount() - 1, 0,
        new QTableWidgetItem(QString::number(pt.x() - 295, 'f', 3)));
    ui->cordtable->setItem(
        ui->cordtable->rowCount() - 1, 1,
        new QTableWidgetItem(QString::number(-1 * (pt.y() - 339), 'f', 3)));
    scene->addEllipse(pt.x() - 12 - 4, pt.y() - 53 - 4, 8, 8, points,
                      fillpoints);
    QGraphicsTextItem *num =
        scene->addText(QString("%1").arg(ui->cordtable->rowCount()), font);
    num->setPos(pt.x() - 12, pt.y() - 53);
    num->setDefaultTextColor(Qt::green);
    state = MOUSE_STATE;
  }
}

void MainWindow::on_undo_triggered() {
  if (state == NO_STATE) {
    return;
  }
  if (state == ADD_STATE) {
    ui->cordtable->removeRow(ui->cordtable->rowCount() - 1);
    redraw();
    state = NO_STATE;
  }
  if (state == CHANGE_STATE) {
    temp_index -= 1;
    ui->cordtable->setItem(
        temp[temp_index].index - 1, 0,
        new QTableWidgetItem(QString::number(temp[temp_index].xc, 'f', 3)));
    ui->cordtable->setItem(
        temp[temp_index].index - 1, 1,
        new QTableWidgetItem(QString::number(temp[temp_index].yc, 'f', 3)));
    redraw();
    state = NO_STATE;
  }
  if (state == DELETE_STATE) {
    temp_index -= 1;
    ui->cordtable->insertRow(ui->cordtable->rowCount());
    ui->cordtable->setItem(
        ui->cordtable->rowCount() - 1, 0,
        new QTableWidgetItem(QString::number(temp[temp_index].xc, 'f', 3)));
    ui->cordtable->setItem(
        ui->cordtable->rowCount() - 1, 1,
        new QTableWidgetItem(QString::number(temp[temp_index].yc, 'f', 3)));
    redraw();
    state = NO_STATE;
  }
  if (state == CLEAR_STATE) {
    for (long i = 1; i <= temp_index; i++) {
      ui->cordtable->insertRow(ui->cordtable->rowCount());
      ui->cordtable->setItem(
          ui->cordtable->rowCount() - 1, 0,
          new QTableWidgetItem(QString::number(temp[i].xc, 'f', 3)));
      ui->cordtable->setItem(
          ui->cordtable->rowCount() - 1, 1,
          new QTableWidgetItem(QString::number(temp[i].yc, 'f', 3)));
    }
    temp_index = 0;
    redraw();
    state = NO_STATE;
  }
  if (state == MOUSE_STATE) {
    ui->cordtable->removeRow(ui->cordtable->rowCount() - 1);
    redraw();
    state = NO_STATE;
  }
}
