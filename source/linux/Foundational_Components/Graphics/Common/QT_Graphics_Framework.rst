..
    This subsection provides details on the QT graphics frameworks

#####################
Qt Graphics Framework
#####################

Qt is a powerful C++ toolkit for writing cross-platform graphics
applications, enabling a single code base to run predictably and perform
well on Windows and embedded platforms,

Please refer `<https://www.qt.io/>`__ for additional details on Qt.

The PSDK target file system includes the pre-built Qt libraries under
:file:`/usr/lib` and a rich set of QT demo applications under
:file:`/usr/share/examples`.

*****
Demos
*****

Demos using the Null Window System / KMS / DRM / EGLFS are
provided with Qt. By default EGLFS will use the ``eglfs_kms`` backend.

.. code-block:: console

   $ /usr/share/examples/opengl/hellogles3/bin/hellogles3 -platform eglfs
   $ /usr/share/examples/opengl/2dpainting/bin/2dpainting -platform eglfs
   $ /usr/share/examples/opengl/openglwindow/bin/openglwindow -platform eglfs

For more information about Qt's EGLFS and using Qt6 in embedded
applications see:

   - https://doc.qt.io/qt-6/embedded-linux.html

******
Qt QPA
******

The Qt6 within PSDK is prebuilt with Wayland enabled and therefore
wayland-egl is the default QPA. Hence all Qt applications should be run
on top of Weston. To run Qt application without Weston, the user can use
``-platform`` option to specify the desired QPA as ``linuxfb`` or ``eglfs``.

.. note::

   The ``linuxfb`` inteface is deprecated and requires switching the display
   into legacy fb mode.

For example:

.. code-block:: console

   $ /usr/share/examples/opengl/2dpainting/bin/2dpainting -platform eglfs

*************************************************
Running Qt Applications with the Weston IVI shell
*************************************************

To run the QT application with ivi-shell, set the
``QT_WAYLAND_SHELL_INTEGRATION`` environment variable to ivi-shell.

.. code-block:: console

   $ export QT_WAYLAND_SHELL_INTEGRATION=ivi-shell

