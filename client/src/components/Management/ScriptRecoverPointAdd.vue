<template>
  <transition name="fade">
    <el-container direction="vertical" v-if="$store.state.isLoaded">
      <!-- 标题区 -->
      <el-header height="60px">
        <h1>
          {{ modeName }}脚本库还原点
        </h1>
      </el-header>

      <!-- 编辑区 -->
      <el-main>
        <el-row :gutter="20">
          <el-col :span="15">
            <div class="common-form">
              <el-form ref="form" :model="form" :rules="formRules" label-width="100px">
                <el-form-item label="说明" prop="note">
                  <el-input
                    type="textarea"
                    resize="none"
                    :autosize="{minRows: 5}"
                    maxlength="200"
                    show-word-limit
                    v-model="form.note"></el-input>
                  <InfoBlock title="有意义的备注可以为将来提供可靠的参考"></InfoBlock>
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
    </el-container>
  </transition>
</template>

<script>
export default {
  name: 'ScriptRecoverPointAdd',
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
        case 'add':
          return await this.addData();
      }
    },
    async addData() {
      let opt = {
        body : {data: this.T.jsonCopy(this.form)},
        alert: {entity: '脚本库还原点', action: '创建', showError: true},
      };

      let apiRes = await this.T.callAPI('post', '/api/v1/script-recover-points/do/add', opt);
      if (!apiRes.ok) return;

      this.$router.push({
        name: 'script-recover-point-list',
      });
    },
  },
  computed: {
    mode() {
      return this.$route.name.split('-').pop();
    },
    modeName() {
      const nameMap = {
        add: '创建',
      };
      return nameMap[this.mode];
    },
  },
  props: {
  },
  data() {
    let userInfoTEXT = this.$store.state.userProfile.name || this.$store.state.userProfile.username;
    return {
      form: {
        note: `${userInfoTEXT} 创建的还原点`,
      },
      formRules: {
        type: [
          {
            trigger : 'change',
            message : '请选择还原点类型',
            required: true,
          },
        ],
        note: [
          {
            trigger : 'change',
            message : '请填写操作备注',
            required: true,
            min     : 1,
          },
        ],
      },
    }
  },
  created() {
    this.$store.commit('updateLoadStatus', true);
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
