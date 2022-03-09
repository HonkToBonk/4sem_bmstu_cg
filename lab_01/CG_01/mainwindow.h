#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QApplication>
#include <QDoubleValidator>
#include <QMainWindow>
#include <QMessageBox>

#include <QDebug>
#include <QGraphicsItem>
#include <QGraphicsScene>
#include <QGraphicsSceneMouseEvent>
#include <QGraphicsTextItem>
#include <QGraphicsView>
#include <QMouseEvent>
#include <QPointF>

#include <cmath>

#define SIZE 1000
#define ANS 3
#define PI 3.1415926535897932
#define SCENERECT 600

#define NO_STATE 0
#define ADD_STATE 1
#define CHANGE_STATE 2
#define DELETE_STATE 3
#define CLEAR_STATE 4
#define MOUSE_STATE 5

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
  Q_OBJECT
public:
  MainWindow(QWidget *parent = nullptr);
  ~MainWindow();

private slots:
  void on_exit_triggered();
  void on_task_triggered();
  void on_reference_triggered();
  void on_undo_triggered();

  void on_addbutton_clicked();
  void on_change_clicked();
  void on_deletepointbutton_clicked();
  void msgbox_wrong_num();

  void on_cordtable_itemSelectionChanged();
  void on_solve_clicked();
  void on_clear_clicked();

  void redraw();
  void mousePressEvent(QMouseEvent *e);

private:
  Ui::MainWindow *ui;
  QGraphicsScene *scene;
};

typedef struct {
  long index;
  double xc;
  double yc;
} cords_t;

typedef struct {
  double rad;
  double xc;
  double yc;
} center_t;

double process(cords_t array[SIZE], int n, cords_t answer[ANS]);
double difference(double a, double b, double c);
double length(double x1, double y1, double x2, double y2);
void outside(cords_t answer[ANS], center_t *outcenter);
void maxcords(cords_t answer[ANS], double *xmax, double *ymax);
void mincords(cords_t answer[ANS], double *xmin, double *ymin);

#endif // MAINWINDOW_H
