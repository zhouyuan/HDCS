#include <hdcs/libhdcs.h>
#include <stdlib.h>

struct hdcs_data {
  hdcs_ioctx_t io;
};

static int hdcs_connect(struct hdcs_data *hdcs)
{
	hdcs_open(&(hdcs->io));
	return 0;

}

static void hdcs_disconnect(struct hdcs_data *hdcs)
{
	if (!hdcs)
		return;

	/* shutdown everything */
  hdcs_close(hdcs->io);
}

int main() {
	struct hdcs_data *hdcs;
	hdcs = (struct hdcs_data*)calloc(1, sizeof(struct hdcs_data));
	if (!hdcs)
		goto failed;

  hdcs_connect(hdcs);
  hdcs_flush_all(hdcs->io);
  hdcs_disconnect(hdcs);
  return 0;

failed:
	if (hdcs)
		free(hdcs);
	return 1;
}
