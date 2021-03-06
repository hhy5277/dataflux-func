<template>
  <transition name="fade">
    <el-container direction="vertical" v-if="$store.state.isLoaded">
      <!-- 标题区 -->
      <el-header height="60px">
        <h1>
          {{ modeName }}脚本包
        </h1>
      </el-header>

      <!-- 编辑区 -->
      <el-main>
        <el-row :gutter="20">
          <el-col :span="15">
            <div class="common-form">
              <el-form ref="form" :model="form" :rules="formRules" label-width="100px">
                <el-form-item label="导入脚本包" prop="upload">
                  <el-upload drag ref="upload" :class="uploadAreaBorderClass"
                    :limit="2"
                    :multiple="false"
                    :auto-upload="false"
                    :show-file-list="false"
                    :http-request="handleUpload"
                    :on-change="onUploadFileChange"
                    :accept="$store.getters.CONFIG('_FUNC_PKG_EXPORT_EXT')"
                    action="">
                    <i class="fa" :class="uploadAreaIconClass"></i>
                    <div class="el-upload__text"><span v-html="uploadAreaIconText"></span></div>
                  </el-upload>
                </el-form-item>

                <el-form-item label="导入令牌" prop="password">
                  <el-input
                    resize="none"
                    maxlength="64"
                    show-word-limit
                    v-model="form.password"></el-input>
                  <InfoBlock title="填写导出时提示的密码，无密码则留空即可"></InfoBlock>
                </el-form-item>

                <el-form-item>
                  <div class="setup-right">
                    <el-button type="primary" @click="submitData">{{ modeName }}</el-button>
                  </div>
                </el-form-item>
              </el-form>
            </div>
          </el-col>
          <el-col :span="9" class="hidden-md-and-down">
          </el-col>
        </el-row>
      </el-main>

      <el-dialog
        title="即将导入脚本包"
        :visible.sync="showConfirm"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        :show-close="false"
        width="750px">
        <span class="import-token-dialog-content">
          <template v-if="checkResult && checkResult.diff">
            <template v-if="!T.isNothing(checkResult.diff.add)">
              <span class="text-good">新增脚本集：</span>
              <el-tag type="success" v-for="d in checkResult.diff.add" :key="d.id">{{ d.title || d.id }}</el-tag>
              <hr class="br">
            </template>

            <template v-if="!T.isNothing(checkResult.diff.replace)">
              <span class="text-watch">替换脚本集：</span>
              <el-tag type="warning" v-for="d in checkResult.diff.replace" :key="d.id">{{ d.title || d.id }}</el-tag>
              <InfoBlock type="warning" title="被替换的脚本集下所有脚本文件会被完整替换为新版本，新版本中不存在的脚本文件会被删除"></InfoBlock>
              <hr class="br">
            </template>
          </template>

          <template v-if="checkResult && checkResult.summary && checkResult.summary.note">
            <span class="text-info">备注：</span>
            <pre class="import-note">{{ checkResult.summary.note }}</pre>
            <hr class="br">
          </template>
        </span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="goBackToList">
            <i class="fa fa-fw fa-arrow-left"></i>
            返回至脚本包导入历史列表
          </el-button>
          <el-button type="primary" @click="confirmImport">
            确认导入
          </el-button>
        </span>
      </el-dialog>
    </el-container>
  </transition>
</template>

<script>
export default {
  name: 'ScriptSetImport',
  components: {
  },
  watch: {
  },
  methods: {
    async submitData() {
      try {
        await this.$refs.form.validate();
      } catch(err) {
        return console.error(err);
      }

      switch(this.mode) {
        case 'import':
          return await this.$refs.upload.submit();
      }
    },
    async handleUpload(req) {
      let bodyData = new FormData();

      let _data = this.T.jsonCopy(this.form);
      for (let k in _data) if (_data.hasOwnProperty(k)) {
        let v = _data[k];
        bodyData.append(k, v);
      }

      bodyData.append('checkOnly', true);
      bodyData.append('files', req.file);

      let opt = {
        body : bodyData,
        alert: {entity: '脚本包', action: '导入'},
      };
      let apiRes = await this.T.callAPI('post', '/api/v1/script-sets/do/import', opt);
      if (!apiRes.ok) {
        return this.alertOnError(apiRes);
      }

      // 打开确认对话框
      this.showConfirm = true;
      this.checkResult = apiRes.data;
    },
    async confirmImport() {
      let opt = {
        body : {confirmId: this.checkResult.confirmId},
        alert: {entity: '脚本包', action: '导入'},
      };
      let apiRes = await this.T.callAPI('post', '/api/v1/script-sets/do/confirm-import', opt);
      if (!apiRes.ok) {
        return this.alertOnError(apiRes);
      }

      this.goBackToList();
    },
    goBackToList() {
      this.$router.push({
        name: 'script-set-import-history-list',
      });
    },
    alertOnError(apiRes) {
      if (apiRes.ok) return;

      switch(apiRes.reason) {
        case 'EBizCondition.InvalidPassword':
          this.$alert(`导入令牌错误<br>
              请尽可能使用复制黏贴的方式填写导入令牌，以避免错填容易混淆的字母数字`, `导入令牌错误`, {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '了解',
            type: 'error',
          });
          break;

        case 'EBizCondition.InvalidOfficialSignature':
          this.$alert(`导入的官方脚本包签名错误<br>
              脚本包可能在复制过程中损坏或遭他人修改，请联系发行方重新提供脚本包`, `官方脚本包签名错误`, {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '了解',
            type: 'error',
          });
          break;

        case 'EBizCondition.ConfirmingImportTimeout':
          this.$alert(`脚本包导入确认超时<br>
              脚本包导入后长时间未确认，请重新尝试导入`, `脚本包导入确认超时`, {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '了解',
            type: 'error',
          });
          break;

        default:
          this.$alert(`脚本包导入时发生意外错误<br>
              请尝试重新导入，如果问题一直出现，请联系脚本包发行方`, `脚本包导入时发生意外错误`, {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '了解',
            type: 'error',
          });
          break;
      }

      this.form.password = '';
      this.initFilePreview();

      setImmediate(() => {
        this.$refs.form.clearValidate();
      });
    },
    initFilePreview() {
      this.$refs.upload.clearFiles();

      this.uploadAreaBorderClass = [];
      this.uploadAreaIconClass   = ['fa-cloud-upload'];
      this.uploadAreaIconText    = `将文件拖到此处，或<em>点击上传</em>`;
    },
    showFilePreview(filename) {
      this.uploadAreaBorderClass = ['upload-area-active'];
      this.uploadAreaIconClass   = ['fa-cloud-upload', 'text-main'];
      this.uploadAreaIconText    = `<code class="text-main">${filename}</code>`;
    },
    onUploadFileChange(file, fileList) {
      if (fileList.length > 1) fileList.splice(0, 1);

      if (fileList.length > 0) {
        this.showFilePreview(fileList[0].name);
      } else {
        this.initFilePreview();
      }
    },
  },
  computed: {
    mode() {
      return this.$route.name.split('-').pop();
    },
    modeName() {
      const nameMap = {
        import: '导入',
      };
      return nameMap[this.mode];
    },
  },
  props: {
  },
  data() {
    return {
      scriptSetMap: {},

      uploadAreaBorderClass: [],
      uploadAreaIconClass  : ['fa-cloud-upload'],
      uploadAreaIconText   : `将文件拖到此处，或<em>点击上传</em>`,

      showConfirm: false,

      checkResult: {},

      form: {
        password: '',
      },
      formRules: {
      },
    }
  },
  created() {
    this.$store.commit('updateLoadStatus', true);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.common-form .el-upload-dragger {
  width: 400px;
}
.el-upload-dragger.upload-area-active {
  border-color: #FF6600 !important;
}
.el-upload-dragger .fa {
  font-size: 67px;
  color: #C0C4CC;
  margin: 40px 0 16px;
  line-height: 50px;
}
</style>
<style scoped>
.import-token-dialog-content {
  display: block;
  font-size: 18px;
  line-height: 50px;
}
.import-token-dialog-content .el-tag+.el-tag {
  margin-left: 10px;
}
.import-note {
  margin: 0;
  padding: 0;
  line-height: 1;
  font-size: 16px;
  padding-left: 20px;
}
</style>
